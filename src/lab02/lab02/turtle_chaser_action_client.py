#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from turtlesim.msg import Pose
from lab02_interfaces.action import ChaseTurtle

class TurtleChaserActionClient(Node):
    def __init__(self):
        super().__init__('turtle_chaser_action_client')

        self.turtle1_pose = None
        self.turtle2_pose = None
        self.goal_in_progress = False

        self._action_client = ActionClient(self, ChaseTurtle, '/chase_turtle')

        # Subscriptions
        self.create_subscription(Pose, '/turtle1/pose', self.turtle1_pose_cb, 10)
        self.create_subscription(Pose, '/turtle2/pose', self.turtle2_pose_cb, 10)

        # 주기적으로 거리 체크
        self.timer = self.create_timer(0.5, self.check_distance_and_send_goal)
        self.get_logger().info('Turtle Chaser Action Client has been started.')

    def turtle1_pose_cb(self, msg):
        self.turtle1_pose = msg

    def turtle2_pose_cb(self, msg):
        self.turtle2_pose = msg

    def check_distance_and_send_goal(self):
        if self.turtle1_pose is None or self.turtle2_pose is None:
            return

        # 이전 Goal이 진행 중이면 새로 요청하지 않음
        if self.goal_in_progress:
            return

        dx = self.turtle1_pose.x - self.turtle2_pose.x
        dy = self.turtle1_pose.y - self.turtle2_pose.y
        distance = math.hypot(dx, dy)

        # 거리가 2.0 이상일 때 Goal 요청
        if distance > 2.0:
            self.send_goal(5.0)

    def send_goal(self, max_time):
        if not self._action_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Action server not available...')
            return

        self.goal_in_progress = True
        goal_msg = ChaseTurtle.Goal()
        goal_msg.max_time_to_travel = float(max_time)

        self.get_logger().info(f'Sending goal with max_time_to_travel = {max_time}s')

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by server.')
            self.goal_in_progress = False
            return

        self.get_logger().info(f'Goal accepted with ID: {goal_handle.goal_id.uuid.tobytes().hex()}')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: Distance = {fb.distance_to_turtle1:.2f}, Time = {fb.time_travelled:.2f}s'
        )

    def get_result_callback(self, future):
        result = future.result().result
        if result.caught:
            self.get_logger().info('Result: Turtle1 WAS CAUGHT!')
        else:
            self.get_logger().info('Result: Turtle1 was NOT caught.')
        
        # 처리 완료 후 다음 요청 가능하도록 해제
        self.goal_in_progress = False

def main(args=None):
    rclpy.init(args=args)
    node = TurtleChaserActionClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()