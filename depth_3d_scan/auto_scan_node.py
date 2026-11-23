#!/usr/bin/env python3
"""
누출 의심 지점 주변을 멈췄다 움직이며 자동 녹화 (LIMO).
  python3 auto_scan_node.py [--ros-args -p pattern:=panorama -p start:=explorer]
start: now(바로) / service(/start_scan) / explorer(auto_explorer 가 가스 탐색을 끝내면)
상태: /scan_status
"""
import math
import os
import signal
import subprocess
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from rcl_interfaces.msg import Log
from std_msgs.msg import String
from std_srvs.srv import Trigger

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_motion import StepExecutor, make_pattern  # noqa: E402

TOPICS = ['/camera/color/image_raw', '/camera/depth/image_raw', '/camera/color/camera_info',
          '/camera/depth/camera_info', '/odom', '/tf', '/tf_static', '/gas/scd41/co2']
# auto_explorer 가 가스 탐색을 끝내고 멈출 때 남기는 로그
EXPLORER_DONE = ('staying stopped', 'Adaptive search stopped')


class AutoScan(Node):
    def __init__(self):
        super().__init__('auto_scan')
        p = self.declare_parameter
        self.pattern = p('pattern', 'panorama').value  # panorama/arc
        self.dwell = p('dwell', 2.0).value  # 멈춤 시간 s
        self.target_dist = p('target_dist', 0.9).value  # arc 반지름 m
        self.start_mode = p('start', 'now').value  # now/service/explorer
        self.record = p('record', True).value
        self.bag_dir = os.path.expanduser(p('bag_dir', '~').value)
        self.bag_name = p('bag_name', '').value  # 비우면 scan_날짜
        self.shrink = p('shrink', True).value
        self.frames = p('frames', 40).value
        self.cmd_topic = p('cmd_vel_topic', '/cmd_vel').value
        # auto_explorer 를 -r /cmd_vel:=<이 토픽> 으로 실행하면, 촬영 중이 아닐 때만 /cmd_vel 로 넘겨줌
        self.explorer_cmd = p('explorer_cmd_topic', '').value
        self.exec = StepExecutor(lin_speed=p('lin_speed', 0.08).value, ang_speed=p('ang_speed', 0.5).value,
                                 front_stop=p('front_stop', 0.30).value)

        self.cmd_pub = self.create_publisher(Twist, self.cmd_topic, 10)
        self.status_pub = self.create_publisher(String, '/scan_status', 10)
        self.create_subscription(Odometry, '/odom', self.on_odom, 20)
        self.create_subscription(LaserScan, '/scan', self.on_scan, qos_profile_sensor_data)
        self.create_service(Trigger, '/start_scan', self.on_start)
        if self.explorer_cmd:
            self.create_subscription(Twist, self.explorer_cmd, self.on_explorer_cmd, 10)
        if self.start_mode == 'explorer':
            self.create_subscription(Log, '/rosout', self.on_rosout, 100)
        self.pose = None
        self.front = None
        self.state, self.t_state = 'idle', time.time()
        self.proc = None
        self.steps, self.k = [], 0
        self.create_timer(0.05, self.tick)
        self.set_status('idle')
        if self.start_mode == 'now':
            self.begin()
        elif self.start_mode == 'explorer':
            self.get_logger().info('대기 중: auto_explorer 가 가스 탐색을 끝내면 시작')
        else:
            self.get_logger().info('대기 중: ros2 service call /start_scan std_srvs/srv/Trigger')

    # ------------------------------------------------------------ 콜백
    def on_odom(self, m):
        q = m.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
        self.pose = (m.pose.pose.position.x, m.pose.pose.position.y, yaw)

    def on_scan(self, m):
        best = None  # 앞 ±20도 최소 거리
        for i, r in enumerate(m.ranges):
            a = m.angle_min + i * m.angle_increment
            if abs(math.atan2(math.sin(a), math.cos(a))) <= math.radians(20) and r > 0.02 and math.isfinite(r):
                best = r if best is None else min(best, r)
        self.front = best

    def busy(self):
        return self.state not in ('idle', 'done', 'error')

    def on_explorer_cmd(self, m):
        if not self.busy():
            self.cmd_pub.publish(m)

    def on_rosout(self, m):
        if m.name.endswith('auto_explorer') and any(k in m.msg for k in EXPLORER_DONE) and not self.busy() \
                and self.state != 'done':
            self.get_logger().info(f'auto_explorer 종료 감지: {m.msg}')
            self.begin()

    def on_start(self, req, res):
        if self.busy():
            res.success, res.message = False, f'이미 진행 중 ({self.state})'
            return res
        self.begin()
        res.success, res.message = True, '촬영 시작'
        return res

    # ------------------------------------------------------------ 진행
    def set_status(self, s):
        self.status_pub.publish(String(data=s))
        self.get_logger().info(f'[상태] {s}')

    def go(self, state):
        self.state, self.t_state = state, time.time()

    def begin(self):
        try:
            self.steps = make_pattern(self.pattern, target_dist=self.target_dist)
        except ValueError as e:
            self.fail(str(e))
            return
        self.k = 0
        self.name = self.bag_name or time.strftime('scan_%Y%m%d_%H%M%S')
        self.path = os.path.join(self.bag_dir, self.name)
        self.go('wait_inputs')

    def fail(self, why):
        self.stop_robot()
        self.stop_record()
        self.set_status(f'error:{why}')
        self.go('error')

    def stop_robot(self):
        self.cmd_pub.publish(Twist())

    def start_record(self):
        if not self.record:
            return
        if os.path.exists(self.path):
            raise RuntimeError(f'{self.path} 가 이미 있습니다')
        self.proc = subprocess.Popen(['ros2', 'bag', 'record', '-o', self.path] + TOPICS,
                                     start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def stop_record(self):
        if self.proc and self.proc.poll() is None:
            os.killpg(self.proc.pid, signal.SIGINT)
            try:
                self.proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(self.proc.pid, signal.SIGKILL)
        self.proc = None

    def topic_ok(self, name):
        return self.count_publishers(name) > 0

    def tick(self):
        now = time.time()
        el = now - self.t_state
        s = self.state
        if s in ('idle', 'done', 'error'):
            return
        if s == 'shrinking':
            if self.shrink_proc.poll() is not None:
                out = self.shrink_proc.stdout.read().strip()
                self.get_logger().info(out)
                self.done(self.small if self.shrink_proc.returncode == 0 else self.path)
            return
        if s == 'wait_inputs':
            missing = [t for t in ('/odom', '/camera/depth/image_raw', '/camera/color/image_raw') if not self.topic_ok(t)]
            if self.pose is not None and not missing:
                if self.count_publishers(self.cmd_topic) > 1:
                    self.get_logger().warn(f'{self.cmd_topic} 를 보내는 노드가 더 있습니다. 촬영 중 명령이 섞일 수 있어요 '
                                           '(auto_explorer 는 -r /cmd_vel:=/cmd_vel_explorer 로 실행).')
                try:
                    self.start_record()
                except Exception as e:  # noqa: BLE001
                    self.fail(str(e))
                    return
                self.origin = self.pose
                self.set_status(f'recording {self.name} ({len(self.steps)} 단계, 패턴 {self.pattern})')
                self.go('warmup')
            elif el > 15:
                self.fail('입력 없음: ' + ', '.join(missing or ['/odom 메시지']))
            return
        if s == 'warmup':  # 녹화 안정 + 첫 지점
            self.stop_robot()
            if el >= 2.0 + self.dwell:
                self.next_step()
            return
        if s == 'move':
            x, y, yaw = self.pose
            v, w, done = self.exec.update(x, y, yaw, self.front, now)
            t = Twist()
            t.linear.x, t.angular.z = float(v), float(w)
            self.cmd_pub.publish(t)
            if done:
                self.stop_robot()
                if self.exec.result:
                    self.get_logger().warn(f'단계 {self.k}/{len(self.steps)}: {self.exec.result}')
                self.go('dwell')
            return
        if s == 'dwell':
            self.stop_robot()
            if el >= self.dwell:
                self.next_step()
            return

    def next_step(self):
        if self.k >= len(self.steps):
            self.finish()
            return
        step = self.steps[self.k]
        self.k += 1
        self.set_status(f'moving {self.k}/{len(self.steps)} {step}')
        self.exec.start(step, self.pose, self.origin, time.time())
        self.go('move')

    def finish(self):
        self.stop_robot()
        self.stop_record()
        if self.record and self.shrink:   # 줄이기는 따로 돌려서 노드가 멈추지 않게
            here = os.path.dirname(os.path.abspath(__file__))
            self.small = self.path + '_small'
            self.shrink_proc = subprocess.Popen(
                [sys.executable, os.path.join(here, 'shrink_bag.py'), self.path, self.small,
                 '--frames', str(self.frames), '--stationary'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.set_status('shrinking')
            self.go('shrinking')
            return
        self.done(self.path)

    def done(self, path):
        self.set_status(f'done:{path}')
        self.go('done')
        if self.record:
            self.get_logger().info(f'노트북으로 옮길 폴더: {path}')

    def destroy_node(self):
        self.stop_robot()
        self.stop_record()
        super().destroy_node()


def main():
    rclpy.init()
    node = AutoScan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
