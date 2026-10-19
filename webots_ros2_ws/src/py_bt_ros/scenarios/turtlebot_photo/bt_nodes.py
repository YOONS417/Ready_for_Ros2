"""
TurtleBot3 + Nav2 사진 촬영 미션용 BT 노드.

  RViz(SetGoal, /bt/goal_pose)
      -> WaitForGoal     : 새 목표를 받으면 목표와 '현재(시작) 위치'를 저장
      -> MoveToGoal      : Nav2 /navigate_to_pose 로 목표 이동   (ROS Action client)
      -> CaptureImage    : /capture_image 서비스로 사진 촬영      (ROS Service client)
      -> ReturnToStart   : 저장해 둔 시작 위치로 복귀             (ROS Action client)

BT 상태는 blackboard 에 저장한다.
  mission_goal  : 받은 목표 (PoseStamped)
  mission_start : 시작 위치 (x, y, qz, qw)  -- map 프레임 기준
  photo_path    : 마지막으로 찍은 사진 경로
"""
from modules.base_bt_nodes import (          # noqa: F401  (제어 노드는 BT 생성기가 이 모듈에서 찾는다)
    BTNodeList, Status, Node, Sequence, Fallback, ReactiveSequence, ReactiveFallback,
)

# ---- BT Node List -------------------------------------------------------
CUSTOM_ACTION_NODES = [
    'MoveToGoal',
    'CaptureImage',
    'ReturnToStart',
]

CUSTOM_CONDITION_NODES = [
    'WaitForGoal',
]

BTNodeList.ACTION_NODES.extend(CUSTOM_ACTION_NODES)
BTNodeList.CONDITION_NODES.extend(CUSTOM_CONDITION_NODES)

# ---- ROS imports --------------------------------------------------------
from rclpy.time import Time
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from std_srvs.srv import Trigger
from tf2_ros import Buffer, TransformListener

from modules.base_bt_nodes_ros import (
    ConditionWithROSTopics,
    ActionWithROSAction,
    ActionWithROSService,
)

# ---- 설정값 (필요하면 여기만 바꾸세요) ------------------------------------
GOAL_TOPIC = '/bt/goal_pose'          # RViz SetGoal 의 Topic
AMCL_TOPIC = '/amcl_pose'             # TF 실패 시 시작 위치를 얻는 예비 경로
NAV_ACTION = '/navigate_to_pose'      # Nav2 action
CAPTURE_SERVICE = '/capture_image'    # capture_image_server.py 가 제공
MAP_FRAME = 'map'
BASE_FRAME = 'base_link'


# ---- 공통 도우미 ---------------------------------------------------------
def _end_mission(bb):
    """미션 상태를 비워서 다음 목표를 받을 수 있게 한다."""
    bb.pop('mission_goal', None)
    bb.pop('mission_start', None)


def _make_nav_goal(x, y, qz, qw, frame_id=MAP_FRAME):
    ps = PoseStamped()
    ps.header.frame_id = frame_id
    # stamp 는 0 으로 둔다. (BT 노드는 시스템 시간, Nav2 는 시뮬레이션 시간을 쓰므로
    # 현재 시각을 찍으면 TF 조회가 실패할 수 있다.)
    ps.pose.position.x = float(x)
    ps.pose.position.y = float(y)
    ps.pose.orientation.z = float(qz)
    ps.pose.orientation.w = float(qw)
    goal = NavigateToPose.Goal()
    goal.pose = ps
    return goal


class _SafeNavAction(ActionWithROSAction):
    """
    베이스의 halt() 는 끝난 goal 에도 매 틱 cancel 을 보낸다 (Sequence 가 실패/성공할 때
    모든 자식에게 halt 를 호출하기 때문). 진행 중일 때만 cancel 하도록 바꾼다.
    """
    def halt(self):
        if self._phase in ('sending', 'running') and self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()
        self._goal_handle = None
        self._phase = 'idle'


# ---- 1) 목표 대기 + 시작 위치 저장 ---------------------------------------
class WaitForGoal(ConditionWithROSTopics):
    """
    새 목표(/bt/goal_pose)가 들어오면 SUCCESS.
    그 순간의 로봇 위치(map 기준)를 mission_start 에 저장한다 -> 나중에 복귀에 사용.
    새 목표가 없으면 FAILURE (Sequence 가 처음부터 다시 기다림).
    """
    def __init__(self, name, agent):
        super().__init__(name, agent, [
            (PoseStamped, GOAL_TOPIC, 'goal'),
            (PoseWithCovarianceStamped, AMCL_TOPIC, 'amcl'),
        ])
        self._consumed = None   # 이미 처리한 목표 메시지 객체
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self.ros.node)

    def _current_pose(self):
        """map 기준 현재 위치 (x, y, qz, qw). TF 가 안 되면 /amcl_pose 로 대체."""
        try:
            t = self._tf_buffer.lookup_transform(MAP_FRAME, BASE_FRAME, Time())
            tr, q = t.transform.translation, t.transform.rotation
            return (tr.x, tr.y, q.z, q.w)
        except Exception:
            pass
        amcl = self._cache.get('amcl')
        if amcl is not None:
            p = amcl.pose.pose
            return (p.position.x, p.position.y, p.orientation.z, p.orientation.w)
        return None

    def _predicate(self, agent, bb):
        goal = self._cache.get('goal')
        if goal is None or goal is self._consumed:
            return False

        start = self._current_pose()
        if start is None:
            self.ros.node.get_logger().warn(
                '시작 위치를 아직 알 수 없습니다 (map->base_link TF 또는 /amcl_pose 없음).',
                throttle_duration_sec=5.0)
            return False       # 목표는 소비하지 않고 다음 틱에 다시 시도

        self._consumed = goal
        bb['mission_goal'] = goal
        bb['mission_start'] = start
        self.ros.node.get_logger().info(
            f"새 목표 수신: ({goal.pose.position.x:.2f}, {goal.pose.position.y:.2f}), "
            f"시작 위치 저장: ({start[0]:.2f}, {start[1]:.2f})")
        return True


# ---- 2) 목표로 이동 ------------------------------------------------------
class MoveToGoal(_SafeNavAction):
    def __init__(self, name, agent):
        super().__init__(name, agent, (NavigateToPose, NAV_ACTION))

    def _build_goal(self, agent, bb):
        g = bb.get('mission_goal')
        if g is None:
            return None
        p = g.pose
        return _make_nav_goal(p.position.x, p.position.y,
                              p.orientation.z, p.orientation.w,
                              g.header.frame_id or MAP_FRAME)

    def _interpret_result(self, result, agent, bb, status_code=None):
        if status_code == GoalStatus.STATUS_SUCCEEDED:
            self.ros.node.get_logger().info('목표 도착')
            return Status.SUCCESS
        self.ros.node.get_logger().warn(f'목표 이동 실패 (status={status_code})')
        _end_mission(bb)
        return Status.FAILURE


# ---- 3) 사진 촬영 --------------------------------------------------------
class CaptureImage(ActionWithROSService):
    """capture_image_server.py 의 /capture_image (std_srvs/Trigger) 를 호출."""
    def __init__(self, name, agent):
        super().__init__(name, agent, (Trigger, CAPTURE_SERVICE))

    def _build_request(self, agent, bb):
        return Trigger.Request()

    def _interpret_response(self, response, agent, bb):
        if response.success:
            bb['photo_path'] = response.message
            self.ros.node.get_logger().info(f'사진 저장: {response.message}')
            return Status.SUCCESS
        self.ros.node.get_logger().warn(f'사진 촬영 실패: {response.message}')
        _end_mission(bb)
        return Status.FAILURE


# ---- 4) 시작 위치로 복귀 -------------------------------------------------
class ReturnToStart(_SafeNavAction):
    def __init__(self, name, agent):
        super().__init__(name, agent, (NavigateToPose, NAV_ACTION))

    def _build_goal(self, agent, bb):
        start = bb.get('mission_start')
        if start is None:
            return None
        x, y, qz, qw = start
        return _make_nav_goal(x, y, qz, qw)

    def _interpret_result(self, result, agent, bb, status_code=None):
        ok = (status_code == GoalStatus.STATUS_SUCCEEDED)
        self.ros.node.get_logger().info('시작 위치로 복귀 완료' if ok
                                        else f'복귀 실패 (status={status_code})')
        _end_mission(bb)      # 성공/실패와 상관없이 다음 목표를 받을 수 있게 정리
        return Status.SUCCESS if ok else Status.FAILURE
