import math
import time
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
from visualization_msgs.msg import Marker, MarkerArray

class SmoothCoverageExplorer(Node):
    """실시간 지도 frontier를 탐색하고 MQ-3 신호를 따라 짧은 이동을 반복한다.

    입력은 `/scan` 장애물 거리, `/map` SLAM 점유격자, `/odom` 자세,
    `/gas/mq3/raw_adc` 원시 센서값이다. 탐색 주행 명령은 `/cmd_vel`로 내보내며,
    지속 감지 시 정지 측정, 변화율 가중 방향 선택, 근거리 이동을 반복한다.
    """

    def __init__(self):
        """ROS 연결, 가스 정지 기준, 탐색 상태와 마커 타이머를 초기화한다."""
        super().__init__('auto_explorer')
        
        scan_qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        
        # 입력: 라이다 거리 배열(/scan), SLAM 격자(/map), 휠/IMU 추정 자세(/odom).
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, scan_qos)
        self.map_sub = self.create_subscription(OccupancyGrid, '/map', self.map_cb, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        # 출력: 탐색 속도 명령(/cmd_vel). 가스 정지 시 이 노드가 0 속도를 발행한다.
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # 이 값은 ppm이 아닌 Arduino ADC count다. 실행 인자로 재정의할 수 있다.
        self.declare_parameter('gas_adc_stop_threshold', 1700)
        self.declare_parameter('gas_adc_release_threshold', 360)
        self.declare_parameter('gas_confirm_samples', 3)
        self.declare_parameter('gas_probe_distance', 0.3)
        self.declare_parameter('gas_probe_settle_sec', 10.0)
        self.declare_parameter('gas_probe_sample_count', 3)
        self.declare_parameter('gas_probe_min_delta', 15)
        self.declare_parameter('gas_probe_rate_weight_sec', 1.0)
        self.declare_parameter('gas_probe_max_rate_gain', 20.0)
        self.declare_parameter('gas_probe_max_moves', 5)
        self.declare_parameter('gas_probe_max_flat_steps', 3)
        self.declare_parameter('gas_probe_heading_change_deg', 137.5)
        self.declare_parameter('gas_probe_arrival_tolerance', 0.05)
        self.declare_parameter('gas_probe_turn_tolerance', 0.08)
        self.declare_parameter('gas_probe_move_timeout_sec', 15.0)
        self.gas_adc_stop_threshold = int(
            self.get_parameter('gas_adc_stop_threshold').value)
        self.gas_adc_release_threshold = int(
            self.get_parameter('gas_adc_release_threshold').value)
        self.gas_confirm_samples = int(
            self.get_parameter('gas_confirm_samples').value)
        self.gas_probe_distance = float(
            self.get_parameter('gas_probe_distance').value)
        self.gas_probe_settle_sec = float(
            self.get_parameter('gas_probe_settle_sec').value)
        self.gas_probe_sample_count = int(
            self.get_parameter('gas_probe_sample_count').value)
        self.gas_probe_min_delta = int(
            self.get_parameter('gas_probe_min_delta').value)
        self.gas_probe_rate_weight_sec = float(
            self.get_parameter('gas_probe_rate_weight_sec').value)
        self.gas_probe_max_rate_gain = float(
            self.get_parameter('gas_probe_max_rate_gain').value)
        self.gas_probe_max_moves = int(
            self.get_parameter('gas_probe_max_moves').value)
        self.gas_probe_max_flat_steps = int(
            self.get_parameter('gas_probe_max_flat_steps').value)
        self.gas_probe_heading_change_deg = float(
            self.get_parameter('gas_probe_heading_change_deg').value)
        self.gas_probe_arrival_tolerance = float(
            self.get_parameter('gas_probe_arrival_tolerance').value)
        self.gas_probe_turn_tolerance = float(
            self.get_parameter('gas_probe_turn_tolerance').value)
        self.gas_probe_move_timeout_sec = float(
            self.get_parameter('gas_probe_move_timeout_sec').value)
        if not 0 <= self.gas_adc_release_threshold < self.gas_adc_stop_threshold <= 1023:
            raise ValueError('gas ADC release threshold must be below stop threshold')
        if (self.gas_confirm_samples < 1 or self.gas_probe_sample_count < 1
                or self.gas_probe_max_moves < 1
                or self.gas_probe_max_flat_steps < 1):
            raise ValueError('gas confirmation and probe sample counts must be positive')
        if (self.gas_probe_distance <= 0.0 or self.gas_probe_settle_sec < 0.0
                or self.gas_probe_arrival_tolerance <= 0.0
                or self.gas_probe_turn_tolerance <= 0.0
                or self.gas_probe_rate_weight_sec < 0.0
                or self.gas_probe_max_rate_gain <= 0.0
                or self.gas_probe_move_timeout_sec <= 0.0
                or self.gas_probe_min_delta < 0):
            raise ValueError('gas probe distances, timeout, and delta are invalid')

        self.gas_state = 'EXPLORING'
        self.gas_high_count = 0
        self.gas_low_count = 0
        self.gas_confirm_readings = []
        self.gas_probe_readings = []
        self.gas_probe_history = []
        self.gas_probe_center_adc = 0.0
        self.gas_probe_previous_adc = 0.0
        self.gas_probe_previous_position = None
        self.gas_probe_best_adc = 0.0
        self.gas_probe_best_position = None
        self.gas_probe_move_count = 0
        self.gas_probe_flat_count = 0
        self.gas_probe_heading = 0.0
        self.gas_probe_last_move_heading = 0.0
        self.gas_probe_settle_started = 0.0
        self.gas_probe_deadline = 0.0
        self.gas_probe_target_yaw = 0.0
        # MQ-3 브리지의 UInt16 원시 ADC 토픽을 받아 위 임계값과 비교한다.
        self.gas_sub = self.create_subscription(
            UInt16, '/gas/mq3/raw_adc', self.gas_adc_cb, 10)
        
        # RViz2 가시화를 위한 MarkerArray 퍼블리셔 추가
        self.marker_pub = self.create_publisher(MarkerArray, '/coverage_markers', 10)

        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_yaw = 0.0
        
        self.mode = 'EXPLORE_FRONTIER'
        self.patrol_cycle = 1
        self.sensor_radius = 1.5  # 가스 센서 감지 반경 (1.5m)
        
        self.target_point = None
        self.target_lock_time = 0.0
        self.blacklist = []
        self.visited_breadcrumbs = []
        
        self.prev_angular_z = 0.0
        self.last_check_x = 0.0
        self.last_check_y = 0.0
        self.stuck_counter = 0
        self.backup_steps = 0
        self.turn_steps = 0
        self.turn_dir = 1.0
        
        # 0.5초마다 RViz 마커 업데이트
        self.marker_timer = self.create_timer(0.5, self.publish_markers)
        
        self.get_logger().info('[가시화 포함] 프론티어 탐색 및 사각지대 순찰 노드를 시작합니다!')

    def publish_markers(self):
        """현재 방문 궤적과 선택된 목표를 RViz MarkerArray로 발행한다.

        위치는 odom 콜백에서 누적한 map 좌표를 사용한다. 초록 원판은 방문
        위치의 센서 커버리지, 노란 구는 현재 탐색 목표를 나타낸다.
        """
        marker_array = MarkerArray()
        now = self.get_clock().now().to_msg()

        # 1. 지나온 궤적(가스 센서 감지 반경)을 초록색 반투명 원판으로 표시
        for i, (vx, vy) in enumerate(self.visited_breadcrumbs):
            m = Marker()
            m.header.frame_id = 'map'
            m.header.stamp = now
            m.ns = 'sensor_coverage'
            m.id = i
            m.type = Marker.CYLINDER
            m.action = Marker.ADD
            m.pose.position.x = float(vx)
            m.pose.position.y = float(vy)
            m.pose.position.z = 0.01
            m.pose.orientation.w = 1.0
            # 지름 = 센서 반경(1.5m) * 2 = 3.0m
            m.scale.x = self.sensor_radius * 2.0
            m.scale.y = self.sensor_radius * 2.0
            m.scale.z = 0.02
            m.color.r = 0.1
            m.color.g = 0.9
            m.color.b = 0.3
            m.color.a = 0.18  # 겹쳐도 지도가 잘 보이도록 반투명 설정
            marker_array.markers.append(m)

        # 2. 현재 향하고 있는 목표 지점을 노란색 구(Sphere)로 표시
        if self.target_point is not None:
            tm = Marker()
            tm.header.frame_id = 'map'
            tm.header.stamp = now
            tm.ns = 'current_target'
            tm.id = 9999
            tm.type = Marker.SPHERE
            tm.action = Marker.ADD
            tm.pose.position.x = float(self.target_point[0])
            tm.pose.position.y = float(self.target_point[1])
            tm.pose.position.z = 0.15
            tm.pose.orientation.w = 1.0
            tm.scale.x = 0.35
            tm.scale.y = 0.35
            tm.scale.z = 0.35
            tm.color.r = 1.0
            tm.color.g = 0.85
            tm.color.b = 0.0
            tm.color.a = 0.9
            marker_array.markers.append(tm)

        self.marker_pub.publish(marker_array)

    def clear_all_markers(self):
        """순찰 회차를 초기화할 때 RViz의 이전 coverage 마커를 삭제한다."""
        marker_array = MarkerArray()
        m = Marker()
        m.header.frame_id = 'map'
        m.action = Marker.DELETEALL
        marker_array.markers.append(m)
        self.marker_pub.publish(marker_array)

    def gas_adc_cb(self, msg):
        """ADC 입력으로 일시 감지/지속 감지를 나누고 정지 측정을 진행한다.

        센서와 토픽은 계속 동작하지만, 정지 후 안정화가 끝난 샘플만
        PROBE_SAMPLING에서 위치별 탐색 데이터로 채택한다.
        """
        adc_value = int(msg.data)

        if self.gas_state == 'EXPLORING':
            if adc_value < self.gas_adc_stop_threshold:
                return
            self.gas_state = 'CONFIRMING'
            self.gas_high_count = 0
            self.gas_low_count = 0
            self.gas_confirm_readings.clear()
            self._clear_motion_state()
            self.get_logger().warning(
                f'MQ-3 ADC {adc_value} >= {self.gas_adc_stop_threshold}; '
                'stopped for confirmation')

        if self.gas_state == 'CONFIRMING':
            self.cmd_pub.publish(Twist())
            if adc_value >= self.gas_adc_stop_threshold:
                self.gas_high_count += 1
                self.gas_low_count = 0
                self.gas_confirm_readings.append(adc_value)
                self.gas_confirm_readings = self.gas_confirm_readings[-self.gas_confirm_samples:]
                if self.gas_high_count >= self.gas_confirm_samples:
                    self._begin_adaptive_search()
            elif adc_value <= self.gas_adc_release_threshold:
                self.gas_low_count += 1
                self.gas_high_count = 0
                self.gas_confirm_readings.clear()
                if self.gas_low_count >= self.gas_confirm_samples:
                    self.gas_state = 'EXPLORING'
                    self.gas_low_count = 0
                    self.get_logger().info(
                        'MQ-3 signal returned below release threshold; '
                        'resuming frontier exploration')
            else:
                self.gas_high_count = 0
                self.gas_low_count = 0
                self.gas_confirm_readings.clear()
            return

        if self.gas_state == 'PROBE_SETTLING':
            if time.monotonic() - self.gas_probe_settle_started < self.gas_probe_settle_sec:
                return
            self.gas_state = 'PROBE_SAMPLING'
            self.gas_probe_readings.clear()

        if self.gas_state == 'PROBE_SAMPLING':
            self.gas_probe_readings.append((adc_value, time.monotonic()))
            if len(self.gas_probe_readings) >= self.gas_probe_sample_count:
                self._process_probe_sample()

    def _clear_motion_state(self):
        """가스 확인 정지 전에 예약된 후진/회전 복구 동작을 취소한다."""
        self.backup_steps = 0
        self.turn_steps = 0
        self.prev_angular_z = 0.0

    def _begin_adaptive_search(self):
        """감지 위치를 기준점으로 기록하고 첫 정지 샘플을 준비한다."""
        self.cmd_pub.publish(Twist())
        self.gas_probe_center_adc = float(np.median(self.gas_confirm_readings))
        self.gas_probe_previous_adc = self.gas_probe_center_adc
        self.gas_probe_previous_position = (self.robot_x, self.robot_y)
        self.gas_probe_best_adc = self.gas_probe_center_adc
        self.gas_probe_best_position = (self.robot_x, self.robot_y)
        self.gas_probe_heading = self.robot_yaw
        self.gas_probe_last_move_heading = self.robot_yaw
        self.gas_probe_move_count = 0
        self.gas_probe_flat_count = 0
        self.gas_probe_history.clear()
        self.gas_probe_readings.clear()
        self.gas_state = 'PROBE_SETTLING'
        self.gas_probe_settle_started = time.monotonic()
        self.get_logger().warning(
            f'Persistent MQ-3 at ADC median={self.gas_probe_center_adc:.0f}; '
            'stopping to measure before adaptive search')

    def _process_probe_sample(self):
        """정지 샘플의 중앙값·변화율·이전 위치 차이로 한 번의 다음 이동을 고른다.

        공간 변화량은 이전 정지 위치의 중앙값과 비교한다. 시간 변화율은
        정지 측정 중 농도가 계속 오르는지 반영해 방향 점수에 가중한다.
        """
        readings = self.gas_probe_readings
        values = [value for value, _ in readings]
        stamps = [stamp for _, stamp in readings]
        median_adc = float(np.median(values))
        elapsed = max(stamps[-1] - stamps[0], 1e-3)
        adc_rate = (values[-1] - values[0]) / elapsed
        position = (self.robot_x, self.robot_y)
        self.gas_probe_history.append({
            'position': position,
            'time': stamps[-1],
            'median_adc': median_adc,
            'rate_adc_per_sec': adc_rate,
        })

        if median_adc > self.gas_probe_best_adc:
            self.gas_probe_best_adc = median_adc
            self.gas_probe_best_position = position

        # 첫 정지 표본은 기준 위치의 센서 추세 확인용이다. 이동 방향 정보가
        # 아직 없으므로 현재 바라보는 쪽으로 한 번만 짧게 이동해 비교를 시작한다.
        if self.gas_probe_move_count == 0:
            self.gas_probe_previous_adc = median_adc
            self.gas_probe_previous_position = position
            self.get_logger().info(
                f'Probe baseline: median={median_adc:.0f}, '
                f'stationary rate={adc_rate:.1f} ADC/s')
            self._start_probe_move(self.robot_yaw)
            return

        previous_position = self.gas_probe_previous_position
        spatial_delta = median_adc - self.gas_probe_previous_adc
        rate_gain = self.gas_probe_rate_weight_sec * adc_rate
        rate_gain = max(
            -self.gas_probe_max_rate_gain,
            min(self.gas_probe_max_rate_gain, rate_gain))
        weighted_gain = spatial_delta + rate_gain
        dx = position[0] - previous_position[0]
        dy = position[1] - previous_position[1]
        moved_distance = math.hypot(dx, dy)
        movement_heading = (
            math.atan2(dy, dx) if moved_distance > 1e-4
            else self.gas_probe_last_move_heading)

        self.get_logger().info(
            f'Probe at ({position[0]:.2f}, {position[1]:.2f}): '
            f'median={median_adc:.0f}, spatial delta={spatial_delta:.0f}, '
            f'rate={adc_rate:.1f} ADC/s, rate gain={rate_gain:.1f}, '
            f'weighted gain={weighted_gain:.1f}')
        self.gas_probe_previous_adc = median_adc
        self.gas_probe_previous_position = position

        if weighted_gain >= self.gas_probe_min_delta:
            self.gas_probe_flat_count = 0
            self.gas_probe_heading = movement_heading
        else:
            self.gas_probe_flat_count += 1
            if self.gas_probe_flat_count >= self.gas_probe_max_flat_steps:
                self._finish_adaptive_search()
                return
            angle = (self.gas_probe_last_move_heading
                     + math.radians(self.gas_probe_heading_change_deg))
            self.gas_probe_heading = math.atan2(math.sin(angle), math.cos(angle))

        if self.gas_probe_move_count >= self.gas_probe_max_moves:
            self._finish_adaptive_search()
            return
        self._start_probe_move(self.gas_probe_heading)

    def _start_probe_move(self, heading):
        """다음 0.3m 이동의 방향을 정하고 필요 시 그 방향으로 제자리 회전한다."""
        self.gas_probe_heading = heading
        self.gas_probe_target_yaw = heading
        yaw_error = math.atan2(
            math.sin(heading - self.robot_yaw),
            math.cos(heading - self.robot_yaw))
        if abs(yaw_error) > self.gas_probe_turn_tolerance:
            self.target_point = None
            self.gas_state = 'PROBE_TURNING'
            self.gas_probe_deadline = (
                time.monotonic() + self.gas_probe_move_timeout_sec)
            self.get_logger().info(
                f'Adjusting search heading by {math.degrees(yaw_error):.1f} degrees')
            return
        self._start_probe_translation()

    def _start_probe_translation(self):
        """현재 위치와 선택 heading으로 단 하나의 가까운 목표를 생성한다."""
        if self.gas_probe_move_count >= self.gas_probe_max_moves:
            self._finish_adaptive_search()
            return

        self.gas_probe_last_move_heading = self.gas_probe_heading
        self.target_point = (
            self.robot_x + self.gas_probe_distance * math.cos(self.gas_probe_heading),
            self.robot_y + self.gas_probe_distance * math.sin(self.gas_probe_heading),
        )
        self.gas_probe_move_count += 1
        self.gas_state = 'PROBE_MOVING'
        self.gas_probe_deadline = (
            time.monotonic() + self.gas_probe_move_timeout_sec)
        self.get_logger().info(
            f'Adaptive move {self.gas_probe_move_count}/'
            f'{self.gas_probe_max_moves} to '
            f'({self.target_point[0]:.2f}, {self.target_point[1]:.2f})')

    def _finish_adaptive_search(self):
        """정체 또는 이동 한도에 도달하면 측정 최고값 위치에서 탐색을 끝낸다."""
        if self.gas_probe_best_position is None:
            self._stop_adaptive_search('no valid probe position')
            return

        distance = math.hypot(
            self.gas_probe_best_position[0] - self.robot_x,
            self.gas_probe_best_position[1] - self.robot_y)
        self.get_logger().warning(
            f'Adaptive search complete: best median ADC='
            f'{self.gas_probe_best_adc:.0f}, '
            f'stopped samples={len(self.gas_probe_history)}')
        if distance <= self.gas_probe_arrival_tolerance:
            self._finish_probe_approach(reached=True)
            return

        self.target_point = self.gas_probe_best_position
        self.gas_state = 'PROBE_APPROACH'
        self.gas_probe_deadline = (
            time.monotonic() + self.gas_probe_move_timeout_sec)

    def _stop_adaptive_search(self, reason):
        """이동/센서 상태가 유효하지 않으면 현재 위치에서 최종 정지한다."""
        self.gas_state = 'GAS_STOPPED'
        self.target_point = None
        self._clear_motion_state()
        self.cmd_pub.publish(Twist())
        self.get_logger().error(f'Adaptive search stopped: {reason}')

    def _finish_probe_approach(self, reached):
        """선택 지점에 도착하거나 timeout이 되면 최종 정지 상태로 전환한다."""
        self.gas_state = 'GAS_STOPPED'
        self.target_point = None
        self._clear_motion_state()
        self.cmd_pub.publish(Twist())
        if reached:
            self.get_logger().error(
                'Reached the best-measured local position; staying stopped')
        else:
            self.get_logger().error(
                'Could not reach the best-measured position before timeout; '
                'staying stopped')

    def _update_probe_motion(self):
        """Odometry 기준 목표 도착/timeout을 처리해 측정 또는 정지 상태로 넘긴다."""
        now = time.monotonic()
        if self.gas_state == 'PROBE_MOVING':
            distance = math.hypot(
                self.target_point[0] - self.robot_x,
                self.target_point[1] - self.robot_y)
            if distance <= self.gas_probe_arrival_tolerance:
                self.gas_state = 'PROBE_SETTLING'
                self.gas_probe_settle_started = now
                self.gas_probe_readings.clear()
                self._clear_motion_state()
                self.cmd_pub.publish(Twist())
                self.get_logger().info(
                    f'Arrived at adaptive sample point; settling for '
                    f'{self.gas_probe_settle_sec:.1f} seconds')
            elif now >= self.gas_probe_deadline:
                self._stop_adaptive_search('timed out moving to sample point')
        elif self.gas_state == 'PROBE_TURNING':
            yaw_error = math.atan2(
                math.sin(self.gas_probe_target_yaw - self.robot_yaw),
                math.cos(self.gas_probe_target_yaw - self.robot_yaw))
            if abs(yaw_error) <= self.gas_probe_turn_tolerance:
                self.cmd_pub.publish(Twist())
                self._start_probe_translation()
            elif now >= self.gas_probe_deadline:
                self._stop_adaptive_search('timed out turning to search heading')
        elif self.gas_state == 'PROBE_APPROACH':
            distance = math.hypot(
                self.target_point[0] - self.robot_x,
                self.target_point[1] - self.robot_y)
            if distance <= self.gas_probe_arrival_tolerance:
                self._finish_probe_approach(reached=True)
            elif now >= self.gas_probe_deadline:
                self._finish_probe_approach(reached=False)

    def odom_cb(self, msg):
        """`/odom` 자세를 갱신하고 0.5m 이상 이동한 위치를 방문 목록에 저장한다."""
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = math.atan2(siny_cosp, cosy_cosp)

        if not self.visited_breadcrumbs or math.hypot(
            self.robot_x - self.visited_breadcrumbs[-1][0],
            self.robot_y - self.visited_breadcrumbs[-1][1]
        ) > 0.5:
            self.visited_breadcrumbs.append((self.robot_x, self.robot_y))
        self._update_probe_motion()

    def is_blacklisted(self, x, y):
        """실패한 목표 주변 1.1m 안에 후보 좌표가 있는지 확인한다."""
        for bx, by in self.blacklist:
            if math.hypot(x - bx, y - by) < 1.1:
                return True
        return False

    def is_covered_by_sensor(self, x, y):
        """후보 좌표가 기존 방문 위치의 1.5m 센서 커버리지 안인지 확인한다."""
        for vx, vy in self.visited_breadcrumbs:
            if math.hypot(x - vx, y - vy) < self.sensor_radius:
                return True
        return False

    def map_cb(self, msg):
        """`/map`을 분석해 다음 탐색 목표를 고른다.

        1) 현재 목표 도달/시간 초과를 갱신한다.
        2) 점유격자를 free, unknown, obstacle로 분류하고 장애물 주변을 제외한다.
        3) 미지 셀과 맞닿은 안전한 free 셀(frontier)을 우선 선택한다.
        4) frontier가 없으면 아직 센서 커버리지에 들지 않은 안전한 free 셀을 고른다.
        5) 격자 인덱스를 map 좌표로 바꾸고 선택 결과를 target_point에 저장한다.

        이 콜백은 목표만 갱신한다. 실제 속도와 장애물 회피는 scan_cb가 담당한다.
        """
        if self.gas_state != 'EXPLORING':
            return

        now = time.time()

        if self.target_point is not None:
            dist_to_target = math.hypot(
                self.target_point[0] - self.robot_x,
                self.target_point[1] - self.robot_y
            )
            if dist_to_target < 0.8:
                self.get_logger().info(f'목표 도달 완료! 다음 구역으로 이동합니다. ({self.mode})')
                self.target_point = None
            elif now - self.target_lock_time > 7.0:
                self.blacklist.append(self.target_point)
                self.target_point = None
            else:
                return

        w, h = msg.info.width, msg.info.height
        res = msg.info.resolution
        ox, oy = msg.info.origin.position.x, msg.info.origin.position.y
        grid = np.array(msg.data, dtype=np.int8).reshape((h, w))

        free_mask = (grid == 0)
        unknown_mask = (grid == -1)
        obstacle_mask = (grid > 50)

        obs_near = obstacle_mask.copy()
        for _ in range(6):
            obs_near |= (
                np.roll(obs_near, 1, axis=0) | np.roll(obs_near, -1, axis=0) |
                np.roll(obs_near, 1, axis=1) | np.roll(obs_near, -1, axis=1)
            )
        safe_free_mask = free_mask & (~obs_near)

        up = np.roll(unknown_mask, -1, axis=0)
        down = np.roll(unknown_mask, 1, axis=0)
        left = np.roll(unknown_mask, -1, axis=1)
        right = np.roll(unknown_mask, 1, axis=1)
        
        frontier_mask = safe_free_mask & (up | down | left | right)
        fy, fx = np.where(frontier_mask)

        best_target = None
        best_score = -999.0

        if len(fx) > 12:
            self.mode = 'EXPLORE_FRONTIER'
            wx = ox + (fx + 0.5) * res
            wy = oy + (fy + 0.5) * res
            dists = np.hypot(wx - self.robot_x, wy - self.robot_y)

            for i in range(0, len(wx), 5):
                d = dists[i]
                if d < 1.2 or d > 7.0 or self.is_blacklisted(wx[i], wy[i]):
                    continue
                angle_to_p = math.atan2(wy[i] - self.robot_y, wx[i] - self.robot_x)
                angle_diff = abs(math.atan2(math.sin(angle_to_p - self.robot_yaw), math.cos(angle_to_p - self.robot_yaw)))
                score = -abs(d - 2.5) - (1.5 * angle_diff)
                if score > best_score:
                    best_score = score
                    best_target = (wx[i], wy[i])

        if best_target is None:
            if self.mode == 'EXPLORE_FRONTIER':
                self.mode = 'PATROL_UNCOVERED'
                self.blacklist.clear()
                self.get_logger().info(
                    f'[Phase 2 전환] 1차 맵핑 완료! 초록색 마커가 닿지 않은 사각지대({self.patrol_cycle}회차)를 탐색합니다.'
                )

            sy, sx = np.where(safe_free_mask)
            if len(sx) == 0:
                return

            for i in range(0, len(sx), 15):
                px = ox + (sx[i] + 0.5) * res
                py = oy + (sy[i] + 0.5) * res
                d = math.hypot(px - self.robot_x, py - self.robot_y)

                if d < 1.0 or self.is_blacklisted(px, py) or self.is_covered_by_sensor(px, py):
                    continue

                angle_to_p = math.atan2(py - self.robot_y, px - self.robot_x)
                angle_diff = abs(math.atan2(math.sin(angle_to_p - self.robot_yaw), math.cos(angle_to_p - self.robot_yaw)))
                score = -d - (1.0 * angle_diff)
                if score > best_score:
                    best_score = score
                    best_target = (px, py)

            if best_target is None:
                self.patrol_cycle += 1
                self.clear_all_markers()
                self.visited_breadcrumbs.clear()
                self.visited_breadcrumbs.append((self.robot_x, self.robot_y))
                self.blacklist.clear()
                self.get_logger().info(
                    f'[전 구역 스캔 완료] 마커를 초기화하고 {self.patrol_cycle}회차 정기 순찰을 시작합니다!'
                )
                return

        self.target_point = best_target
        self.target_lock_time = now
        self.get_logger().info(f'[{self.mode}] 새 목표 설정: ({best_target[0]:.2f}, {best_target[1]:.2f})')

    def scan_cb(self, msg):
        """`/scan` 거리와 현재 목표를 이용해 한 번의 `/cmd_vel`을 계산한다.

        가스 정지가 래치된 경우 항상 0 속도를 발행한다. 그 외에는 전방/좌우
        장애물, stuck 복구 상태, 목표 방향과 열린 공간을 반영해 주행한다.
        """
        if self.gas_state in (
            'CONFIRMING', 'PROBE_SETTLING', 'PROBE_SAMPLING', 'GAS_STOPPED'):
            self.cmd_pub.publish(Twist())
            return

        n = len(msg.ranges)
        c = n // 2
        
        def get_clean(arr):
            valid = [r for r in arr if not math.isnan(r) and not math.isinf(r) and r > 0.02]
            return valid if valid else [10.0]

        front_dist = min(get_clean(msg.ranges[c - 35 : c + 35]))
        left_dist = min(get_clean(msg.ranges[c + 35 : c + 105]))
        right_dist = min(get_clean(msg.ranges[c - 105 : c - 35]))

        if self.gas_state == 'PROBE_TURNING':
            if min(front_dist, left_dist, right_dist) < 0.30:
                self._stop_adaptive_search(
                    'obstacle too close to safely rotate in place')
                return
            yaw_error = math.atan2(
                math.sin(self.gas_probe_target_yaw - self.robot_yaw),
                math.cos(self.gas_probe_target_yaw - self.robot_yaw))
            twist = Twist()
            twist.angular.z = max(-0.4, min(0.4, 1.2 * yaw_error))
            self.cmd_pub.publish(twist)
            return

        if self.gas_state in ('PROBE_MOVING', 'PROBE_APPROACH'):
            if front_dist < 0.30:
                self._stop_adaptive_search(
                    'obstacle too close during adaptive probe movement')
                return
            dx = self.target_point[0] - self.robot_x
            dy = self.target_point[1] - self.robot_y
            distance = math.hypot(dx, dy)
            target_yaw = math.atan2(dy, dx)
            yaw_error = math.atan2(
                math.sin(target_yaw - self.robot_yaw),
                math.cos(target_yaw - self.robot_yaw))
            twist = Twist()
            if abs(yaw_error) > self.gas_probe_turn_tolerance:
                # Align in place before translating; this keeps each sample hop local.
                twist.angular.z = max(-0.35, min(0.35, 1.0 * yaw_error))
            else:
                twist.linear.x = min(0.10, max(0.04, 0.6 * distance))
                twist.angular.z = max(-0.15, min(0.15, 0.8 * yaw_error))
            self.cmd_pub.publish(twist)
            return

        sectors = [
            np.mean(get_clean(msg.ranges[c - 100 : c - 60])),
            np.mean(get_clean(msg.ranges[c - 60 : c - 20])),
            np.mean(get_clean(msg.ranges[c - 20 : c + 20])),
            np.mean(get_clean(msg.ranges[c + 20 : c + 60])),
            np.mean(get_clean(msg.ranges[c + 60 : c + 100]))
        ]
        sector_angles = [-0.85, -0.42, 0.0, 0.42, 0.85]
        open_space_angle = sector_angles[int(np.argmax(sectors))]

        twist = Twist()

        if self.backup_steps > 0:
            self.backup_steps -= 1
            twist.linear.x = -0.24
            twist.linear.y = 0.14 if self.turn_dir > 0 else -0.14
            twist.angular.z = 0.0
            self.prev_angular_z = 0.0
            self.cmd_pub.publish(twist)
            return

        if self.turn_steps > 0:
            self.turn_steps -= 1
            twist.linear.x = 0.0
            twist.angular.z = self.turn_dir * 0.85
            self.prev_angular_z = twist.angular.z
            self.cmd_pub.publish(twist)
            return

        probe_motion = self.gas_state in ('PROBE_MOVING', 'PROBE_APPROACH')
        if not probe_motion:
            self.stuck_counter += 1
        if not probe_motion and self.stuck_counter >= 15:
            moved_dist = math.hypot(self.robot_x - self.last_check_x, self.robot_y - self.last_check_y)
            self.last_check_x = self.robot_x
            self.last_check_y = self.robot_y
            self.stuck_counter = 0
            
            if moved_dist < 0.05:
                if self.target_point is not None:
                    self.blacklist.append(self.target_point)
                    self.target_point = None
                self.turn_dir = 1.0 if left_dist >= right_dist else -1.0
                self.backup_steps = 12
                self.turn_steps = 12
                return

        if front_dist < 0.38 or left_dist < 0.24 or right_dist < 0.24:
            if probe_motion:
                self._stop_adaptive_search(
                    'obstacle too close during adaptive movement')
                return
            self.turn_dir = 1.0 if left_dist >= right_dist else -1.0
            self.backup_steps = 8
            self.turn_steps = 10
            return

        if front_dist < 0.75:
            twist.linear.x = 0.08
            raw_angular = 0.85 if left_dist >= right_dist else -0.85
        else:
            twist.linear.x = 0.26
            if self.target_point is not None:
                tx, ty = self.target_point
                target_yaw = math.atan2(ty - self.robot_y, tx - self.robot_x)
                angle_err = math.atan2(math.sin(target_yaw - self.robot_yaw), math.cos(target_yaw - self.robot_yaw))
                raw_angular = (0.60 * angle_err) + (0.40 * open_space_angle)
            else:
                raw_angular = 0.65 * open_space_angle

            if right_dist < 0.55:
                raw_angular += 0.55 * (0.55 - right_dist)
            if left_dist < 0.55:
                raw_angular -= 0.55 * (0.55 - left_dist)

        smoothed_angular = (0.55 * self.prev_angular_z) + (0.45 * raw_angular)
        twist.angular.z = max(-0.75, min(0.75, smoothed_angular))
        self.prev_angular_z = twist.angular.z

        self.cmd_pub.publish(twist)

def main(args=None):
    """탐색 노드를 시작하고 종료 시 마지막 0 속도 명령을 발행한다."""
    rclpy.init(args=args)
    node = SmoothCoverageExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()