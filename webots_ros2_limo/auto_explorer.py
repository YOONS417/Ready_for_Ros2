import math
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker, MarkerArray


class SmoothCoverageExplorer(Node):
    """실시간 SLAM 지도(/map)와 라이다(/scan)를 이용해 공간을 자율 탐색하는 노드.

    동작 단계:
      - Phase 1 (EXPLORE_FRONTIER): 미탐색 경계선(Frontier)을 우선 개척해 지도를 완성
      - Phase 2 (PATROL_UNCOVERED): 지도는 밝혀졌으나 가스 센서 반경이 닿지 않은 사각지대 방문
      - Phase 3 (순찰 리셋): 전 구역 스캔 완료 시 방문 기록과 마커를 초기화하고 정기 순찰 반복
    """

    def __init__(self):
        super().__init__('auto_explorer')

        # LIMO 라이다(/scan) 토픽은 BEST_EFFORT QoS를 사용하므로 호환되도록 설정
        scan_qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        # 토픽 구독: 라이다 거리(/scan), SLAM 격자 지도(/map), 로봇 위치·자세(/odom)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, scan_qos)
        self.map_sub = self.create_subscription(OccupancyGrid, '/map', self.map_cb, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        # 토픽 발행: 로봇 속도 명령(/cmd_vel), RViz2 시각화 마커(/coverage_markers)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/coverage_markers', 10)

        # 로봇의 현재 위치(x, y)와 바라보는 방향 각도(yaw, 라디안)
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_yaw = 0.0

        # 탐색 모드 및 커버리지 파라미터
        self.mode = 'EXPLORE_FRONTIER'  # 현재 탐색 단계 ('EXPLORE_FRONTIER' 또는 'PATROL_UNCOVERED')
        self.patrol_cycle = 1           # 정기 순찰 회차 카운터
        self.sensor_radius = 1.5        # 가스 센서 유효 감지 반경 (m)

        # 목표 지점 관리 및 진척도 기반 타임아웃 상태 변수
        self.target_point = None              # 현재 고정된 목표 좌표 (x, y)
        self.target_lock_time = 0.0           # 현재 목표를 처음 설정한 시각 (초)
        self.last_progress_time = 0.0         # 마지막으로 목표에 유의미하게 가까워진 시각 (초)
        self.best_target_dist = float('inf')  # 현재 목표 설정 이후 기록한 최단 거리 (m)

        # 타임아웃 기준 파라미터
        self.progress_timeout = 5.0      # 진척 없을 때 포기할 시간 (초)
        self.max_target_timeout = 30.0   # 한 목표에 허용하는 절대 최대 시간 (초)
        self.min_progress_dist = 0.25    # 진척으로 인정할 최소 거리 감소량 (m)

        # 탐색 이력 관리 리스트
        self.blacklist = []            # 도달 실패(막힘/끼임)로 판정된 목표 좌표 목록
        self.visited_breadcrumbs = []  # 로봇이 실제로 지나간 위치 (x, y) 궤적

        # 주행 스무딩 및 물리적 끼임 탈출 상태 변수
        self.prev_angular_z = 0.0  # 직전 프레임의 회전 각속도 (로우패스 필터용)
        self.last_check_x = 0.0    # 끼임 판정 시 이전 비교 기준 x좌표
        self.last_check_y = 0.0    # 끼임 판정 시 이전 비교 기준 y좌표
        self.stuck_counter = 0     # 끼임 판정 주기 카운터 (/scan 10Hz 기준 15회 ≈ 1.5초)
        self.backup_steps = 0      # 탈출 1단계(후진) 남은 스텝 수
        self.turn_steps = 0        # 탈출 2단계(제자리 회전) 남은 스텝 수
        self.turn_dir = 1.0        # 탈출 회전 방향 (+1.0: 좌회전, -1.0: 우회전)

        # 0.5초(2Hz) 주기로 RViz2에 커버리지 및 목표 마커 발행
        self.marker_timer = self.create_timer(0.5, self.publish_markers)

        self.get_logger().info('[가시화+진척도 타임아웃] 프론티어 탐색 및 사각지대 순찰 노드를 시작합니다!')

    def _now_sec(self):
        """ROS 2 시계 기준 현재 시각을 초(float) 단위로 반환 (시뮬레이션 시간 동기화)."""
        return self.get_clock().now().nanoseconds * 1e-9

    def publish_markers(self):
        """방문한 가스 센서 감지 영역(초록 원판)과 현재 목표 지점(노란 구)을 RViz2에 표시."""
        marker_array = MarkerArray()
        now = self.get_clock().now().to_msg()

        # 1. 로봇이 지나온 궤적마다 가스 센서 반경(1.5m) 크기의 초록색 반투명 원판 생성
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
            m.pose.position.z = 0.01  # 지도 바닥면 바로 위에 배치
            m.pose.orientation.w = 1.0
            # 원판 지름 = 센서 반경 * 2 (3.0m)
            m.scale.x = self.sensor_radius * 2.0
            m.scale.y = self.sensor_radius * 2.0
            m.scale.z = 0.02
            m.color.r = 0.1
            m.color.g = 0.9
            m.color.b = 0.3
            m.color.a = 0.18  # 여러 원이 겹쳐도 지도가 비치도록 반투명 설정
            marker_array.markers.append(m)

        # 2. 현재 로봇이 향하고 있는 목표 좌표를 노란색 구(Sphere)로 표시
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
        """순찰 회차가 초기화될 때 RViz2 화면에 남아있는 기존 마커를 모두 삭제."""
        marker_array = MarkerArray()
        m = Marker()
        m.header.frame_id = 'map'
        m.action = Marker.DELETEALL
        marker_array.markers.append(m)
        self.marker_pub.publish(marker_array)

    def odom_cb(self, msg):
        """/odom 토픽에서 로봇의 현재 위치와 방향(yaw)을 갱신하고 방문 궤적을 기록."""
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

        # 쿼터니언(x, y, z, w)을 2D 평면 회전각(yaw)으로 변환
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = math.atan2(siny_cosp, cosy_cosp)

        # 직전 기록 위치로부터 0.5m 이상 이동했을 때만 새 방문 궤적 추가 (리스트 과다 증가 방지)
        if not self.visited_breadcrumbs or math.hypot(
            self.robot_x - self.visited_breadcrumbs[-1][0],
            self.robot_y - self.visited_breadcrumbs[-1][1]
        ) > 0.5:
            self.visited_breadcrumbs.append((self.robot_x, self.robot_y))

    def is_blacklisted(self, x, y):
        """후보 좌표 (x, y)가 과거 실패한 블랙리스트 좌표 반경 1.1m 이내인지 확인."""
        for bx, by in self.blacklist:
            if math.hypot(x - bx, y - by) < 1.1:
                return True
        return False

    def is_covered_by_sensor(self, x, y):
        """후보 좌표 (x, y)가 이미 지나온 궤적의 가스 센서 반경(1.5m) 안에 포함되는지 확인."""
        for vx, vy in self.visited_breadcrumbs:
            if math.hypot(x - vx, y - vy) < self.sensor_radius:
                return True
        return False

    def map_cb(self, msg):
        """/map 점유격자를 분석해 다음 목표 지점(target_point)을 선정하는 콜백.

        실제 모터 제어(/cmd_vel)는 scan_cb가 담당하며, 여기서는 목표 좌표만 관리한다.
        """
        now = self._now_sec()

        # ------------------------------------------------------------------
        # 1. 현재 진행 중인 목표 지점의 도착 여부 및 진척도/시간 초과 검사
        # ------------------------------------------------------------------
        if self.target_point is not None:
            dist_to_target = math.hypot(
                self.target_point[0] - self.robot_x,
                self.target_point[1] - self.robot_y
            )
            # 목표 반경 0.8m 이내 진입 시 도착 완료 처리
            if dist_to_target < 0.8:
                self.get_logger().info(f'목표 도달 완료! 다음 구역으로 이동합니다. ({self.mode})')
                self.target_point = None
                self.best_target_dist = float('inf')
            else:
                # 기존 최단 기록보다 0.25m 이상 더 가까워졌을 때만 진척 인정 및 타이머 리셋
                if dist_to_target < self.best_target_dist - self.min_progress_dist:
                    self.best_target_dist = dist_to_target
                    self.last_progress_time = now

                no_progress_elapsed = now - self.last_progress_time
                total_elapsed = now - self.target_lock_time

                # 일정 시간 동안 가까워지지 못하면 장애물 막힘으로 판단해 포기
                if no_progress_elapsed > self.progress_timeout:
                    self.get_logger().info(
                        f'목표 접근 진척 없음({no_progress_elapsed:.1f}초) -> 블랙리스트 등록 후 새 목표 탐색'
                    )
                    self.blacklist.append(self.target_point)
                    self.target_point = None
                    self.best_target_dist = float('inf')
                # 너무 큰 우회 등으로 절대 최대 시간을 초과하면 포기
                elif total_elapsed > self.max_target_timeout:
                    self.get_logger().info(
                        f'목표 최대 주행 시간 초과({total_elapsed:.1f}초) -> 블랙리스트 등록 후 새 목표 탐색'
                    )
                    self.blacklist.append(self.target_point)
                    self.target_point = None
                    self.best_target_dist = float('inf')
                else:
                    # 정상적으로 접근 중이면 기존 목표 유지 (갈팡질팡 방지)
                    return

        # ------------------------------------------------------------------
        # 2. 점유격자(/map) 파싱 및 안전 영역(safe_free_mask) 계산
        # ------------------------------------------------------------------
        w, h = msg.info.width, msg.info.height
        res = msg.info.resolution  # 셀 1칸당 실제 크기 (보통 0.05m)
        ox, oy = msg.info.origin.position.x, msg.info.origin.position.y  # 지도 원점 좌표
        grid = np.array(msg.data, dtype=np.int8).reshape((h, w))

        # Cartographer 확률값(0~49)을 빈 공간으로, -1을 미지 공간으로, >50을 장애물로 분류
        free_mask = (grid >= 0) & (grid < 50)
        unknown_mask = (grid == -1)
        obstacle_mask = (grid > 50)

        # 장애물 마스크를 상하좌우로 4칸(약 20cm) 팽창시켜 벽 바로 옆은 목표 후보에서 제외
        obs_near = obstacle_mask.copy()
        for _ in range(4):
            obs_near |= (
                np.roll(obs_near, 1, axis=0) | np.roll(obs_near, -1, axis=0) |
                np.roll(obs_near, 1, axis=1) | np.roll(obs_near, -1, axis=1)
            )
        safe_free_mask = free_mask & (~obs_near)

        # ------------------------------------------------------------------
        # 3. [Phase 1] 프론티어(안전한 빈 공간과 미지 공간의 경계선) 검출 및 선택
        # ------------------------------------------------------------------
        # 상하좌우 인접 셀 중 하나라도 미지 공간(-1)인 위치 추출
        up = np.roll(unknown_mask, -1, axis=0)
        down = np.roll(unknown_mask, 1, axis=0)
        left = np.roll(unknown_mask, -1, axis=1)
        right = np.roll(unknown_mask, 1, axis=1)

        frontier_mask = safe_free_mask & (up | down | left | right)
        fy, fx = np.where(frontier_mask)

        best_target = None
        best_score = -999.0

        # 유효 프론티어 픽셀이 6개 이상 남아있으면 Phase 1 수행
        if len(fx) > 5:
            self.mode = 'EXPLORE_FRONTIER'
            # 픽셀 인덱스를 실제 map 좌표계(m)로 변환
            wx = ox + (fx + 0.5) * res
            wy = oy + (fy + 0.5) * res
            dists = np.hypot(wx - self.robot_x, wy - self.robot_y)

            # 연산 부하를 줄이기 위해 5개 픽셀 간격으로 샘플링하여 최적 후보 평가
            for i in range(0, len(wx), 5):
                d = dists[i]
                # 너무 가깝거나(<0.8m) 너무 먼(>12.0m) 점, 블랙리스트 근처는 제외
                if d < 0.8 or d > 12.0 or self.is_blacklisted(wx[i], wy[i]):
                    continue
                # 로봇 정면 방향과의 각도 차이 계산 (-pi ~ pi 정규화)
                angle_to_p = math.atan2(wy[i] - self.robot_y, wx[i] - self.robot_x)
                angle_diff = abs(math.atan2(math.sin(angle_to_p - self.robot_yaw), math.cos(angle_to_p - self.robot_yaw)))
                # 적정 거리(2.5m)에 가깝고 회전이 적게 필요한(정면 방향) 목표에 높은 점수 부여
                score = -abs(d - 2.5) - (1.5 * angle_diff)
                if score > best_score:
                    best_score = score
                    best_target = (wx[i], wy[i])

        # ------------------------------------------------------------------
        # 4. [Phase 2] 프론티어가 없으면 가스 센서 미탐지 사각지대 탐색
        # ------------------------------------------------------------------
        if best_target is None:
            if self.mode == 'EXPLORE_FRONTIER':
                self.mode = 'PATROL_UNCOVERED'
                self.blacklist.clear()  # 1차 탐색 블랙리스트 초기화
                self.get_logger().info(
                    f'[Phase 2 전환] 1차 맵핑 완료! 초록색 마커가 닿지 않은 사각지대({self.patrol_cycle}회차)를 탐색합니다.'
                )

            sy, sx = np.where(safe_free_mask)
            if len(sx) == 0:
                return

            # 안전한 빈 공간을 15픽셀 간격으로 샘플링해 아직 방문하지 않은 지점 검색
            for i in range(0, len(sx), 15):
                px = ox + (sx[i] + 0.5) * res
                py = oy + (sy[i] + 0.5) * res
                d = math.hypot(px - self.robot_x, py - self.robot_y)

                # 너무 가깝거나 블랙리스트이거나 이미 센서 반경(1.5m)으로 훑은 곳은 제외
                if d < 1.0 or self.is_blacklisted(px, py) or self.is_covered_by_sensor(px, py):
                    continue

                angle_to_p = math.atan2(py - self.robot_y, px - self.robot_x)
                angle_diff = abs(math.atan2(math.sin(angle_to_p - self.robot_yaw), math.cos(angle_to_p - self.robot_yaw)))
                # 가장 가깝고 회전이 적은 사각지대 우선 선택
                score = -d - (1.0 * angle_diff)
                if score > best_score:
                    best_score = score
                    best_target = (px, py)

            # --------------------------------------------------------------
            # 5. [Phase 3] 모든 사각지대까지 스캔 완료 시 방문 기록 리셋 후 재순찰
            # --------------------------------------------------------------
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

        # 선정된 새 목표를 고정하고 타임아웃·진척도 기준값 초기화
        self.target_point = best_target
        self.target_lock_time = now
        self.last_progress_time = now
        self.best_target_dist = math.hypot(
            best_target[0] - self.robot_x,
            best_target[1] - self.robot_y
        )
        self.get_logger().info(
            f'[{self.mode}] 새 목표 설정: ({best_target[0]:.2f}, {best_target[1]:.2f}) | 거리: {self.best_target_dist:.2f}m'
        )

    def scan_cb(self, msg):
        """/scan 라이다 데이터를 이용해 장애물 회피, 끼임 탈출, 목표 추종 속도를 계산."""
        n = len(msg.ranges)
        c = n // 2  # 정면 중앙 빔 인덱스

        def get_clean(arr):
            """NaN, 무한대, 2cm 이하 노이즈를 제외한 유효 거리 리스트 반환."""
            valid = [r for r in arr if not math.isnan(r) and not math.isinf(r) and r > 0.02]
            return valid if valid else [10.0]

        # 전방, 좌측, 우측 영역의 최단 장애물 거리 추출
        front_dist = min(get_clean(msg.ranges[c - 35 : c + 35]))
        left_dist = min(get_clean(msg.ranges[c + 35 : c + 105]))
        right_dist = min(get_clean(msg.ranges[c - 105 : c - 35]))

        # 전방 시야를 5개 구역(우측, 우전방, 정면, 좌전방, 좌측)으로 나누어 가장 넓게 뚫린 방향 계산
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

        # ------------------------------------------------------------------
        # 1. [자가 복구 1단계] 직선 후진 + 메카넘 횡이동으로 벽에서 분리
        # ------------------------------------------------------------------
        if self.backup_steps > 0:
            self.backup_steps -= 1
            twist.linear.x = -0.24
            twist.linear.y = 0.14 if self.turn_dir > 0 else -0.14  # 넓은 쪽으로 살짝 밀어냄
            twist.angular.z = 0.0
            self.prev_angular_z = 0.0
            self.cmd_pub.publish(twist)
            return

        # ------------------------------------------------------------------
        # 2. [자가 복구 2단계] 확보된 공간에서 넓은 쪽으로 제자리 회전
        # ------------------------------------------------------------------
        if self.turn_steps > 0:
            self.turn_steps -= 1
            twist.linear.x = 0.0
            twist.angular.z = self.turn_dir * 0.85
            self.prev_angular_z = twist.angular.z
            self.cmd_pub.publish(twist)
            return

        # ------------------------------------------------------------------
        # 3. [물리적 끼임 감지] 15스텝(약 1.5초) 동안 5cm 미만 이동 시 강제 탈출
        # ------------------------------------------------------------------
        self.stuck_counter += 1
        if self.stuck_counter >= 15:
            moved_dist = math.hypot(self.robot_x - self.last_check_x, self.robot_y - self.last_check_y)
            self.last_check_x = self.robot_x
            self.last_check_y = self.robot_y
            self.stuck_counter = 0

            if moved_dist < 0.05:
                # 끼임을 유발한 현재 목표는 블랙리스트에 등록하고 포기
                if self.target_point is not None:
                    self.blacklist.append(self.target_point)
                    self.target_point = None
                    self.best_target_dist = float('inf')
                self.turn_dir = 1.0 if left_dist >= right_dist else -1.0
                self.backup_steps = 12
                self.turn_steps = 12
                return

        # ------------------------------------------------------------------
        # 4. [초근접 위험 회피] 벽에 너무 바짝 붙으면 즉시 후진+회전 예약
        # ------------------------------------------------------------------
        if front_dist < 0.38 or left_dist < 0.24 or right_dist < 0.24:
            self.turn_dir = 1.0 if left_dist >= right_dist else -1.0
            self.backup_steps = 8
            self.turn_steps = 10
            return

        # ----------------------------------ros2 run webots_ros2_limo auto_explorer --------------------------------
        # 5. [일반 주행] 전방 장애물 회피 또는 하이브리드 목표 추종
        # ------------------------------------------------------------------
        if front_dist < 0.75:
            # 전방 0.75m 이내 장애물 감지 시 저속으로 넓은 쪽을 향해 회전
            twist.linear.x = 0.08
            raw_angular = 0.85 if left_dist >= right_dist else -0.85
        else:
            twist.linear.x = 0.26
            if self.target_point is not None:
                # 목표 방향(60%) + 라이다 최대 개방 공간 방향(40%) 결합 조향
                tx, ty = self.target_point
                target_yaw = math.atan2(ty - self.robot_y, tx - self.robot_x)
                angle_err = math.atan2(math.sin(target_yaw - self.robot_yaw), math.cos(target_yaw - self.robot_yaw))
                raw_angular = (0.60 * angle_err) + (0.40 * open_space_angle)
            else:
                # 목표가 아직 없으면 가장 넓은 공간 방향으로 이동
                raw_angular = 0.65 * open_space_angle

            # 측면 벽 반발력 보정 (벽에서 0.55m 이상 거리를 유지하도록 밀어냄)
            if right_dist < 0.55:
                raw_angular += 0.55 * (0.55 - right_dist)
            if left_dist < 0.55:
                raw_angular -= 0.55 * (0.55 - left_dist)

        # 로우패스 스무딩 필터 적용 (이전 각속도 55% + 새 각속도 45%)으로 좌우 떨림 완화
        smoothed_angular = (0.55 * self.prev_angular_z) + (0.45 * raw_angular)
        twist.angular.z = max(-0.75, min(0.75, smoothed_angular))
        self.prev_angular_z = twist.angular.z

        self.cmd_pub.publish(twist)


def main(args=None):
    """ROS 2 노드 초기화 및 실행. 종료 시 안전하게 로봇 정지 명령을 발행."""
    rclpy.init(args=args)
    node = SmoothCoverageExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # 노드 종료 시 바퀴가 계속 굴러가지 않도록 0 속도 발행
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
