import math
from modules.base_bt_nodes import BTNodeList, Status, Node, Sequence, Fallback, ReactiveSequence, ReactiveFallback

# 1. 과제용 커스텀 노드 리스트 등록
CUSTOM_ACTION_NODES = [
    'MoveToGoal',
    'CaptureImage',
    'Return'
]

CUSTOM_CONDITION_NODES = [
    # 필요시 조건 노드 추가
]

BTNodeList.ACTION_NODES.extend(CUSTOM_ACTION_NODES)
BTNodeList.CONDITION_NODES.extend(CUSTOM_CONDITION_NODES)

from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
from sensor_msgs.msg import Image
from modules.base_bt_nodes_ros import ActionWithROSAction, ActionWithROSService, ConditionWithROSTopics
import cv2
from cv_bridge import CvBridge

# -------------------------------------------------------------
# 1단계: MoveToGoal (RViz /bt/goal_pose -> Nav2 /navigate_to_pose)
# -------------------------------------------------------------
class MoveToGoal(ActionWithROSAction):
    def __init__(self, *args, **kwargs):
        agent = kwargs.get('agent') or (args[1] if len(args) > 1 else None)
        super().__init__(args[0] if args else 'MoveToGoal', agent, (NavigateToPose, 'navigate_to_pose'))
        
        self.target_pose = None
        self.current_amcl_pose = None
        
        # /amcl_pose를 구독하여 로봇의 현재 실시간 위치를 추적 (초기 위치 저장용)
        self.ros.node.create_subscription(
            PoseWithCovarianceStamped, '/amcl_pose', self._amcl_callback, 10
        )
        # RViz 커스텀 툴(/bt/goal_pose) 구독
        self.ros.node.create_subscription(
            PoseStamped, '/bt/goal_pose', self._goal_callback, 10
        )

    def _amcl_callback(self, msg):
        # AMCL을 통해 들어오는 현재 로봇의 포즈를 계속 백업
        self.current_amcl_pose = msg.pose.pose

    def _goal_callback(self, msg):
        self.target_pose = msg

    def _build_goal(self, agent, bb):
        if self.target_pose is None:
            return None
        
        # 블랙보드에 초기 위치('initial_pose')가 아직 없다면, 
        # 이동을 시작하는 이 시점의 로봇 현재 위치(AMCL Pose)를 초기 위치로 저장!
        if 'initial_pose' not in bb and self.current_amcl_pose is not None:
            init_ps = PoseStamped()
            init_ps.header.frame_id = 'map'
            init_ps.header.stamp = self.ros.node.get_clock().now().to_msg()
            init_ps.pose = self.current_amcl_pose
            bb['initial_pose'] = init_ps
            print(f"[MoveToGoal] 초기 출발 위치 저장 완료: x={init_ps.pose.position.x}, y={init_ps.pose.position.y}")

        goal = NavigateToPose.Goal()
        goal.pose = self.target_pose
        return goal

    def _interpret_result(self, result, agent, bb, status_code=None):
        if status_code == GoalStatus.STATUS_SUCCEEDED:
            bb['move_status'] = 'success'
            # 다음 단계를 위해 target_pose 초기화 (다음 실행 시 재입력 대기)
            self.target_pose = None
            return Status.SUCCESS
        return Status.FAILURE


# -------------------------------------------------------------
# 2단계: CaptureImage (카메라 이미지 수신 및 저장)
# -------------------------------------------------------------
class CaptureImage(Node):
    def __init__(self, *args, **kwargs):
        name = args[0] if args else 'CaptureImage'
        super().__init__(name)
        self.bridge = CvBridge()
        self.latest_image = None
        
        agent = kwargs.get('agent') or (args[1] if len(args) > 1 else None)
        if agent:
            # 프레임워크의 ros_bridge를 통해 안전하게 구독 생성
            ros_bridge = agent.ros_bridge
            ros_bridge.node.create_subscription(
                Image, '/TurtleBot3Burger/front_camera/image_color', self._image_callback, 10
            )

    def _image_callback(self, msg):
        self.latest_image = msg

    async def run(self, agent, blackboard):
        if self.latest_image is not None:
            try:
                # ROS 이미지 메시지를 OpenCV 이미지로 변환 후 저장
                cv_image = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
                cv2.imwrite('captured_image.png', cv_image)
                print("[CaptureImage] 사진 촬영 및 저장 완료!")
                return Status.SUCCESS
            except Exception as e:
                print(f"[CaptureImage] 에러 발생: {e}")
                return Status.FAILURE
        
        # 아직 이미지가 안 들어왔다면 대기(RUNNING)
        self.status = Status.RUNNING
        return self.status


# -------------------------------------------------------------
# 3단계: Return (저장해둔 초기 위치로 복귀)
# -------------------------------------------------------------
class Return(ActionWithROSAction):
    def __init__(self, *args, **kwargs):
        agent = kwargs.get('agent') or (args[1] if len(args) > 1 else None)
        super().__init__(args[0] if args else 'Return', agent, (NavigateToPose, 'navigate_to_pose'))
        
    def _build_goal(self, agent, bb):
        initial_pose = bb.get('initial_pose')
        if initial_pose is None:    
            print("[Return] 에러: 저장된 초기 위치(initial_pose)가 없습니다!")
            return None
        
        goal = NavigateToPose.Goal()
        goal.pose = initial_pose  # 1단계 시작 때 저장해둔 처음 위치로 설정
        return goal

    def _interpret_result(self, result, agent, bb, status_code=None):
        if status_code == GoalStatus.STATUS_SUCCEEDED:
            print("[Return] 원래 위치로 복귀 성공!")
            return Status.SUCCESS
        print(f"[Return] 복귀 실패 (status_code: {status_code})")
        return Status.FAILURE