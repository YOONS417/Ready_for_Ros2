import time
import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import UInt16

class SCD41SerialBridge(Node):
    """Arduino SCD41 시리얼 출력(CO2 ppm)을 ROS 2 토픽으로 전달하는 노드."""

    def __init__(self):
        super().__init__('scd41_serial_bridge')
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('poll_rate', 10.0)  # SCD41은 데이터 업데이트가 느림 (약 2초 주기)

        self.port = self.get_parameter('port').value
        self.baud_rate = self.get_parameter('baud_rate').value
        poll_rate = self.get_parameter('poll_rate').value

        # SCD41의 CO2 ppm 값을 발행 (MQ-3의 ADC를 대체)
        self.co2_pub = self.create_publisher(UInt16, '/gas/scd41/co2', 10)

        self.serial_port = None
        self.rx_buffer = bytearray()
        self.next_connect_attempt = 0.0
        self.timer = self.create_timer(1.0 / poll_rate, self.poll_serial)
        
        self.get_logger().info(f'SCD41 serial bridge waiting for {self.port} at {self.baud_rate} baud')

    def connect_serial(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baud_rate, timeout=0)
            self.rx_buffer.clear()
            self.get_logger().info(f'Connected to SCD41 Arduino on {self.port}')
        except serial.SerialException as exc:
            self.next_connect_attempt = time.monotonic() + 2.0
            self.get_logger().warning(f'Cannot open {self.port}: {exc}')

    def poll_serial(self):
        if self.serial_port is None:
            if time.monotonic() >= self.next_connect_attempt:
                self.connect_serial()
            if self.serial_port is None:
                return

        try:
            waiting = self.serial_port.in_waiting
            data = self.serial_port.read(waiting if waiting else 1)
        except serial.SerialException as exc:
            self.get_logger().warning(f'SCD41 serial connection lost: {exc}')
            self.close_serial()
            self.next_connect_attempt = time.monotonic() + 2.0
            return

        if not data:
            return

        self.rx_buffer.extend(data)
        if len(self.rx_buffer) > 512:
            self.rx_buffer.clear()
            return

        while b'\n' in self.rx_buffer:
            line, _, remaining = self.rx_buffer.partition(b'\n')
            self.rx_buffer = bytearray(remaining)
            self.publish_reading(line.decode('ascii', errors='ignore').strip())

    def publish_reading(self, line):
        try:
            # Arduino는 오직 CO2 ppm 정수값만 Serial.println()으로 전송함
            co2_val = int(line)
            msg = UInt16()
            msg.data = co2_val
            self.co2_pub.publish(msg)
        except ValueError:
            # 숫자가 아닌 문자열(에러 메시지 등)은 무시
            return

    def close_serial(self):
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None

    def destroy_node(self):
        self.close_serial()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = SCD41SerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
