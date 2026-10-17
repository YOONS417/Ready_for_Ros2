import math
import random
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # 속도 데이터 토픽 타입 추가
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill, SetPen  # SetPen 서비스 추가

class CatchTurtleNode(Node):
    def __init__(self):
        super().__init__('catch_turtle_node')

        self.player_pose = None
        self.target_pose = None
        self.target_name = 'target_turtle'
        self.is_spawning = False
        self.score = 0
        
        # 펜 상태 추적 변수 ('red', 'blue', 'none')
        self.current_pen_color = 'none'

        # 1. Subscriber: 위치 및 이동 속도(cmd_vel) 구독
        self.create_subscription(Pose, '/turtle1/pose', self.player_pose_callback, 10)
        self.create_subscription(Twist, '/turtle1/cmd_vel', self.cmd_vel_callback, 10)

        # 2. Service Clients: Spawn, Kill, SetPen
        self.spawn_client = self.create_client(Spawn, 'spawn')
        self.kill_client = self.create_client(Kill, 'kill')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('loading Spawn service ...')

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('loading SetPen service ...')

        self.create_timer(0.1, self.check_catch_loop)
        self.spawn_target_turtle()

    def player_pose_callback(self, msg):
        self.player_pose = msg

    def target_pose_callback(self, msg):
        self.target_pose = msg

    def cmd_vel_callback(self, msg):
        # linear.x > 0: 전진 (빨간색), linear.x < 0: 후진 (파란색)
        if msg.linear.x > 0 and self.current_pen_color != 'red':
            self.change_pen_color(255, 0, 0, 3)  # Red: R=255, G=0, B=0, 두께=3
            self.current_pen_color = 'red'
        elif msg.linear.x < 0 and self.current_pen_color != 'blue':
            self.change_pen_color(0, 0, 255, 3)  # Blue: R=0, G=0, B=255, 두께=3
            self.current_pen_color = 'blue'

    def change_pen_color(self, r, g, b, width):
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = 0  # 펜 켜기 (0)
        self.pen_client.call_async(req)

    def spawn_target_turtle(self):
        if self.is_spawning:
            return
        self.is_spawning = True

        req = Spawn.Request()
        req.x = random.uniform(1.0, 10.0)
        req.y = random.uniform(1.0, 10.0)
        req.theta = random.uniform(0.0, 2 * math.pi)
        req.name = self.target_name

        future = self.spawn_client.call_async(req)
        future.add_done_callback(self.spawn_callback)

    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'respawn new turtle : {response.name}')
            self.create_subscription(
                Pose, f'/{self.target_name}/pose', self.target_pose_callback, 10
            )
            self.is_spawning = False
        except Exception as e:
            self.get_logger().error(f'fail to respawn: {e}')
            self.is_spawning = False

    def kill_target_turtle(self):
        req = Kill.Request()
        req.name = self.target_name

        future = self.kill_client.call_async(req)
        future.add_done_callback(self.kill_callback)

    def kill_callback(self, future):
        try:
            future.result()
            self.score += 1
            self.get_logger().info(f'catch turtle! current socre : {self.score}점')
            self.target_pose = None
            self.spawn_target_turtle()
        except Exception as e:
            self.get_logger().error(f'fail to elmenate: {e}')

    def check_catch_loop(self):
        if self.player_pose is None or self.target_pose is None or self.is_spawning:
            return

        dx = self.target_pose.x - self.player_pose.x
        dy = self.target_pose.y - self.player_pose.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < 0.8:
            self.kill_target_turtle()

def main(args=None):
    rclpy.init(args=args)
    node = CatchTurtleNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()