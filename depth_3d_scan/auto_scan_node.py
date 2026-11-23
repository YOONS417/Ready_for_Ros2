#!/usr/bin/env python3
"""
누출 의심 지점 주변을 멈췄다 움직이며 자동 녹화 (LIMO). 끝나면 shrink_bag.py 로 줄임.
  python3 auto_scan_node.py [--ros-args -p pattern:=arc -p start:=explorer -p explorer_cmd_topic:=/cmd_vel_explorer]
pattern: panorama(제자리 30도씩 한 바퀴) / arc(앞 물체 주위 ±30도)
start:   now / service(/start_scan) / explorer(auto_explorer 가 가스 탐색을 끝내면)
상태:    /scan_status (recording → moving k/n → shrinking → done:<경로> | error:<이유>)
"""
import math
import os
import signal
import subprocess
import sys
import time

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rcl_interfaces.msg import Log
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_srvs.srv import Trigger

TOPICS = ['/camera/color/image_raw', '/camera/depth/image_raw', '/camera/color/camera_info',
          '/camera/depth/camera_info', '/odom', '/tf', '/tf_static', '/gas/scd41/co2']
EXPLORER_DONE = ('staying stopped', 'Adaptive search stopped')   # auto_explorer 가 멈출 때 남기는 로그
LIN, ANG = 0.08, 0.5                  # m/s, rad/s
FRONT_STOP = 0.30                     # 직진 중 앞 라이다 거리가 이보다 가까우면 그 단계 중단 (m)
YAW_TOL, POS_TOL, STEP_TIMEOUT = math.radians(2), 0.02, 25.0
HERE = os.path.dirname(os.path.abspath(__file__))


def wrap(a):
    return math.atan2(math.sin(a), math.cos(a))


def make_pattern(name, r=0.9):
    """('turn', 도) 제자리 회전 / ('goto', x, y, 도) — 모두 시작 자세 기준이라 오차가 쌓이지 않음."""
    if name == 'panorama':            # 화각 66도라 30도씩 돌면 반씩 겹침
        return [('turn', 30 * k) for k in range(1, 12)]
    if name == 'arc':                 # 물체 = 시작 위치 앞 r, 원 위에서 물체를 바라봄
        return [('goto', r - r * math.cos(math.radians(a)), -r * math.sin(math.radians(a)), a)
                for a in (-15, -30, 15, 30)]
    raise ValueError(f'모르는 패턴: {name} (panorama / arc)')


class Step:
    """한 단계를 odom 으로 실행. update() → (v, w, done)."""

    def __init__(self, step, origin, now):
        self.step, self.t0, self.phase, self.result = step, now, 0, ''
        ox, oy, oyaw = origin
        self.goal_yaw = wrap(oyaw + math.radians(step[-1]))
        if step[0] == 'goto':
            _, gx, gy, _ = step
            self.gx = ox + gx * math.cos(oyaw) - gy * math.sin(oyaw)
            self.gy = oy + gx * math.sin(oyaw) + gy * math.cos(oyaw)

    @staticmethod
    def turn_to(yaw, target):
        e = wrap(target - yaw)
        return (0.0, True) if abs(e) <= YAW_TOL else (math.copysign(max(0.15, min(ANG, 1.5 * abs(e))), e), False)

    def update(self, x, y, yaw, front, now):
        if now - self.t0 > STEP_TIMEOUT:
            self.result = 'timeout'
            return 0.0, 0.0, True
        if self.step[0] == 'goto' and self.phase < 2:      # 돌기 → 직진 → (아래) 방향 맞추기
            dist = math.hypot(self.gx - x, self.gy - y)
            head = math.atan2(self.gy - y, self.gx - x)
            if dist <= POS_TOL:
                self.phase = 2
            elif self.phase == 0:
                w, ok = self.turn_to(yaw, head)
                if not ok:
                    return 0.0, w, False
                self.phase = 1
            else:
                if front is not None and front < FRONT_STOP:
                    self.result = f'blocked(front {front:.2f} m)'
                    return 0.0, 0.0, True
                e = wrap(head - yaw)
                if abs(e) > math.radians(25):              # 많이 틀어지면 다시 돌기
                    self.phase = 0
                    return 0.0, 0.0, False
                return min(LIN, max(0.03, 1.2 * dist)), 1.5 * e, False
        w, ok = self.turn_to(yaw, self.goal_yaw)
        return 0.0, w, ok


class AutoScan(Node):
    def __init__(self):
        super().__init__('auto_scan')
        p = lambda n, d: self.declare_parameter(n, d).value   # noqa: E731
        self.pattern, self.start_mode = p('pattern', 'panorama'), p('start', 'now')
        self.dwell, self.target_dist = p('dwell', 2.0), p('target_dist', 0.9)
        self.record, self.bag_name = p('record', True), p('bag_name', '')
        self.shrink, self.frames = p('shrink', True), p('frames', 40)
        explorer_cmd = p('explorer_cmd_topic', '')   # explorer 를 -r /cmd_vel:=<이 토픽> 으로 실행했을 때

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/scan_status', 10)
        self.create_subscription(Odometry, '/odom', self.on_odom, 20)
        self.create_subscription(LaserScan, '/scan', self.on_scan, qos_profile_sensor_data)
        self.create_service(Trigger, '/start_scan', self.on_start)
        if explorer_cmd:   # 촬영 중이 아닐 때만 explorer 명령을 /cmd_vel 로 넘겨줌
            self.create_subscription(Twist, explorer_cmd, lambda m: self.busy() or self.cmd_pub.publish(m), 10)
        if self.start_mode == 'explorer':
            self.create_subscription(Log, '/rosout', self.on_rosout, 100)
        self.pose = self.front = self.proc = None
        self.state, self.t_state = 'idle', time.time()
        self.create_timer(0.05, self.tick)
        self.set_status('idle')
        if self.start_mode == 'now':
            self.begin()

    def on_odom(self, m):
        q = m.pose.pose.orientation
        self.pose = (m.pose.pose.position.x, m.pose.pose.position.y,
                     math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z)))

    def on_scan(self, m):   # 앞 ±20도 최소 거리 (0 = 무효값)
        r = np.asarray(m.ranges)
        a = np.arctan2(np.sin(m.angle_min + np.arange(len(r)) * m.angle_increment),
                       np.cos(m.angle_min + np.arange(len(r)) * m.angle_increment))
        r = r[(np.abs(a) <= math.radians(20)) & (r > 0.02) & np.isfinite(r)]
        self.front = float(r.min()) if len(r) else None

    def on_rosout(self, m):
        if m.name.endswith('auto_explorer') and any(k in m.msg for k in EXPLORER_DONE) and self.state == 'idle':
            self.begin()

    def on_start(self, req, res):
        res.success = not self.busy()
        res.message = '촬영 시작' if res.success else f'이미 진행 중 ({self.state})'
        if res.success:
            self.begin()
        return res

    def busy(self):
        return self.state not in ('idle', 'done', 'error')

    def set_status(self, s):
        self.status_pub.publish(String(data=s))
        self.get_logger().info(f'[상태] {s}')

    def go(self, state):
        self.state, self.t_state = state, time.time()

    def begin(self):
        try:
            self.steps, self.k = make_pattern(self.pattern, self.target_dist), 0
        except ValueError as e:
            return self.fail(str(e))
        self.path = os.path.join(os.path.expanduser('~'), self.bag_name or time.strftime('scan_%Y%m%d_%H%M%S'))
        self.go('wait_inputs')

    def fail(self, why):
        self.stop_record()
        self.set_status(f'error:{why}')
        self.go('error')

    def stop_record(self):
        self.cmd_pub.publish(Twist())
        if self.proc and self.proc.poll() is None:
            os.killpg(self.proc.pid, signal.SIGINT)
            try:
                self.proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(self.proc.pid, signal.SIGKILL)
        self.proc = None

    def tick(self):
        el, s = time.time() - self.t_state, self.state
        if s == 'wait_inputs':
            missing = [t for t in ('/odom', '/camera/depth/image_raw', '/camera/color/image_raw')
                       if self.count_publishers(t) == 0]
            if self.pose is None or missing:
                if el > 15:
                    self.fail('입력 없음: ' + ', '.join(missing or ['/odom 메시지']))
                return
            if self.count_publishers('/cmd_vel') > 1:
                self.get_logger().warn('/cmd_vel 을 보내는 노드가 더 있습니다 '
                                       '(auto_explorer 는 -r /cmd_vel:=/cmd_vel_explorer 로 실행).')
            if self.record:
                if os.path.exists(self.path):
                    return self.fail(f'{self.path} 가 이미 있습니다')
                self.proc = subprocess.Popen(['ros2', 'bag', 'record', '-o', self.path] + TOPICS,
                                             start_new_session=True, stdout=subprocess.DEVNULL,
                                             stderr=subprocess.STDOUT)
            self.origin = self.pose
            self.set_status(f'recording {os.path.basename(self.path)} ({len(self.steps)} 단계, {self.pattern})')
            self.go('dwell')
            self.t_state += 2.0                      # 첫 지점: 녹화가 자리 잡을 시간 2초 더
        elif s == 'move':
            v, w, done = self.cur.update(*self.pose, self.front, time.time())
            t = Twist()
            t.linear.x, t.angular.z = float(v), float(w)
            self.cmd_pub.publish(t)
            if done:
                if self.cur.result:
                    self.get_logger().warn(f'단계 {self.k}/{len(self.steps)}: {self.cur.result}')
                self.go('dwell')
        elif s == 'dwell':
            self.cmd_pub.publish(Twist())
            if el >= self.dwell:
                if self.k < len(self.steps):
                    self.cur = Step(self.steps[self.k], self.origin, time.time())
                    self.k += 1
                    self.set_status(f'moving {self.k}/{len(self.steps)}')
                    self.go('move')
                else:
                    self.finish()
        elif s == 'shrinking' and self.shrink_proc.poll() is not None:
            self.get_logger().info(self.shrink_proc.stdout.read().strip())
            self.done(self.path + '_small' if self.shrink_proc.returncode == 0 else self.path)

    def finish(self):
        self.stop_record()
        if self.record and self.shrink:              # 줄이기는 따로 돌려서 노드가 멈추지 않게
            self.shrink_proc = subprocess.Popen(
                [sys.executable, os.path.join(HERE, 'shrink_bag.py'), self.path, self.path + '_small',
                 '--frames', str(self.frames), '--stationary'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.set_status('shrinking')
            self.go('shrinking')
        else:
            self.done(self.path)

    def done(self, path):
        self.set_status(f'done:{path}')
        self.go('done')


def main():
    rclpy.init()
    node = AutoScan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_record()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
