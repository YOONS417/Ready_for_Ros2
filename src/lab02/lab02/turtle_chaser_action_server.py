#!/usr/bin/env python3
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, SetPen

# 인터페이스 패키지명에 맞춰 수정 (예: lab02_interfaces 또는 ros_lab_interfaces)
from lab02_interfaces.action import ChaseTurtle

class TurtleChaserActionServer(Node):
    def __init__(self):
        super().__init__('turtle_chaser_action_server')
        self.cb_group = ReentrantCallbackGroup()

        self.turtle1_pose = None
        self.turtle2_pose = None

        # 1. Pose Subscriptions
        self.create_subscription(Pose, '/turtle1/pose', self.turtle1_pose_cb, 10, callback_group=self.cb_group)
        self.create_subscription(Pose, '/turtle2/pose', self.turtle2_pose_cb, 10, callback_group=self.cb_group)

        # 2. Velocity Publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        # 3. Spawn turtle2
        self.spawn_turtle2()

        # 4. (선택사항) 펜 색상 설정
        self.set_pen_colors()

        # 5. Action Server Creation
        self._action_server = ActionServer(
            self,
            ChaseTurtle,
            '/chase_turtle',
            execute_callback=self.execute_callback,
            callback_group=self.cb_group
        )
        self.get_logger().info('Turtle Chaser Action Server has been started.')

    def turtle1_pose_cb(self, msg):
        self.turtle1_pose = msg

    def turtle2_pose_cb(self, msg):
        self.turtle2_pose = msg

    def spawn_turtle2(self):
        client = self.create_client(Spawn, '/spawn', callback_group=self.cb_group)
        if not client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('Spawn service not available.')
            return
        
        req = Spawn.Request()
        req.x = 1.0
        req.y = 10.0
        req.theta = 0.0
        req.name = 'turtle2'
        
        future = client.call_async(req)
        # 서비스 호출 완료까지 대기하지 않고 비동기 처리
        self.get_logger().info('Successfully requested to spawn turtle2')

    def set_pen_colors(self):
        # turtle1 red trail, turtle2 blue trail
        cli1 = self.create_client(SetPen, '/turtle1/set_pen', callback_group=self.cb_group)
        cli2 = self.create_client(SetPen, '/turtle2/set_pen', callback_group=self.cb_group)
        
        if cli1.wait_for_service(timeout_sec=2.0):
            req1 = SetPen.Request(r=255, g=0, b=0, width=3, off=0)
            cli1.call_async(req1)
            
        if cli2.wait_for_service(timeout_sec=2.0):
            req2 = SetPen.Request(r=0, g=0, b=255, width=3, off=0)
            cli2.call_async(req2)

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing turtle chase...')
        
        max_time = goal_handle.request.max_time_to_travel
        start_time = time.time()
        
        feedback_msg = ChaseTurtle.Feedback()
        result = ChaseTurtle.Result()

        rate = self.create_rate(10) # 10Hz 제어 루프

        while rclpy.ok():
            elapsed_time = time.time() - start_time

            if self.turtle1_pose is None or self.turtle2_pose is None:
                rate.sleep()
                continue

            # 거리 계산
            dx = self.turtle1_pose.x - self.turtle2_pose.x
            dy = self.turtle1_pose.y - self.turtle2_pose.y
            distance = math.hypot(dx, dy)

            # 피드백 전송
            feedback_msg.distance_to_turtle1 = float(distance)
            feedback_msg.time_travelled = float(elapsed_time)
            goal_handle.publish_feedback(feedback_msg)

            # 성공 조건: 거리가 0.5 미만
            if distance < 0.5:
                # 정지
                self.cmd_vel_pub.publish(Twist())
                goal_handle.succeed()
                result.caught = True
                self.get_logger().info('Successfully caught turtle1!')
                return result

            # 실패 조건: 제한 시간 초과
            if elapsed_time > max_time:
                self.cmd_vel_pub.publish(Twist())
                goal_handle.succeed()
                result.caught = False
                self.get_logger().info('Max time reached. Turtle1 not caught.')
                return result

            # P-Control (turtle2가 turtle1을 추적하도록 이동)
            angle_to_target = math.atan2(dy, dx)
            angle_diff = angle_to_target - self.turtle2_pose.theta

            # 각도 정규화 (-pi ~ pi)
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            twist = Twist()
            twist.linear.x = min(1.5 * distance, 2.0)
            twist.angular.z = 4.0 * angle_diff
            self.cmd_vel_pub.publish(twist)

            rate.sleep()

def main(args=None):
    rclpy.init(args=args)
    node = TurtleChaserActionServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()