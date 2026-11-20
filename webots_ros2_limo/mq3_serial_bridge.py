"""Arduino MQ-3 시리얼 측정값을 ROS 2 가스 토픽으로 전달한다.

입력: Uno가 시리얼로 보내는 `MQ3,<sequence>,<adc>` 한 줄 메시지.
출력: `/gas/mq3/raw_adc`, `/gas/mq3/voltage`, 보정 설정 시
`/gas/mq3/ethanol_ppm`.
"""

import time

import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32, UInt16


def build_calibration_points(adc_values, ppm_values):
    """ROS 파라미터 보정 배열을 검증하고 ADC 순으로 정렬한다.

    ADC와 이에 대응하는 알려진 에탄올 ppm을 같은 인덱스끼리 짝짓는다.
    보정점이 두 개 미만이면 ppm 계산을 비활성화하기 위해 빈 목록을 반환한다.
    """
    if len(adc_values) != len(ppm_values):
        raise ValueError('calibration_adc and calibration_ppm must have equal lengths')
    if len(adc_values) < 2:
        return []

    points = sorted((int(adc), float(ppm))
                    for adc, ppm in zip(adc_values, ppm_values))
    if any(adc < 0 or adc > 1023 for adc, _ in points):
        raise ValueError('calibration_adc values must be between 0 and 1023')
    if any(ppm < 0.0 for _, ppm in points):
        raise ValueError('calibration_ppm values cannot be negative')
    if any(points[i][0] == points[i - 1][0]
           for i in range(1, len(points))):
        raise ValueError('calibration_adc values must be unique')

    ppm_steps = [points[i][1] - points[i - 1][1]
                 for i in range(1, len(points))]
    if not (all(step > 0.0 for step in ppm_steps)
            or all(step < 0.0 for step in ppm_steps)):
        raise ValueError('calibration_ppm must change monotonically with ADC')
    return points


def interpolate_ethanol_ppm(adc_value, calibration_points):
    """보정점 사이의 ADC를 선형 보간해 ppm으로 변환한다.

    입력 ADC가 보정 구간 밖이면 외삽하지 않고 None을 반환한다. 실제 ppm의
    정확도는 MQ-3와 회로, 환경에 맞는 실측 보정점에 의존한다.
    """
    if len(calibration_points) < 2:
        return None

    for (low_adc, low_ppm), (high_adc, high_ppm) in zip(
            calibration_points, calibration_points[1:]):
        if low_adc <= adc_value <= high_adc:
            ratio = (adc_value - low_adc) / (high_adc - low_adc)
            return low_ppm + ratio * (high_ppm - low_ppm)
    return None


class MQ3SerialBridge(Node):
    """Arduino USB 시리얼 입력을 ROS 측정 토픽으로 변환하는 노드.

    Arduino가 한 줄을 보낼 때마다 raw ADC와 전압을 발행한다. 유효한
    보정점이 설정된 경우에만 보정 범위 안의 샘플에 대해 ppm도 발행한다.
    """

    def __init__(self):
        """포트·baud·보정 파라미터와 토픽, 시리얼 폴링 타이머를 준비한다."""
        super().__init__('mq3_serial_bridge')
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 9600)
        self.declare_parameter('adc_reference_voltage', 5.0)
        self.declare_parameter('poll_rate', 50.0)
        self.declare_parameter('calibration_adc', [0])
        self.declare_parameter('calibration_ppm', [0.0])

        self.port = self.get_parameter('port').value
        self.baud_rate = self.get_parameter('baud_rate').value
        self.adc_reference_voltage = self.get_parameter(
            'adc_reference_voltage').value
        poll_rate = self.get_parameter('poll_rate').value
        self.calibration_points = build_calibration_points(
            self.get_parameter('calibration_adc').value,
            self.get_parameter('calibration_ppm').value)
        if self.adc_reference_voltage <= 0.0 or poll_rate <= 0.0:
            raise ValueError('adc_reference_voltage and poll_rate must be positive')

        self.raw_pub = self.create_publisher(UInt16, '/gas/mq3/raw_adc', 10)
        self.voltage_pub = self.create_publisher(Float32, '/gas/mq3/voltage', 10)
        self.ethanol_pub = self.create_publisher(
            Float32, '/gas/mq3/ethanol_ppm', 10)

        self.serial_port = None
        self.rx_buffer = bytearray()
        self.next_connect_attempt = 0.0
        self.outside_calibration_range = False
        self.timer = self.create_timer(1.0 / poll_rate, self.poll_serial)
        self.get_logger().info(
            f'MQ-3 serial bridge waiting for {self.port} at {self.baud_rate} baud')
        if not self.calibration_points:
            self.get_logger().warning(
                'No MQ-3 calibration configured; raw ADC and voltage will publish, '
                'but ethanol_ppm will not')

    def connect_serial(self):
        """설정된 Arduino 포트를 연다. 실패하면 타이머가 재연결을 시도한다."""
        try:
            self.serial_port = serial.Serial(
                self.port, self.baud_rate, timeout=0)
            self.rx_buffer.clear()
            self.get_logger().info(f'Connected to MQ-3 Arduino on {self.port}')
        except serial.SerialException as exc:
            self.next_connect_attempt = time.monotonic() + 2.0
            self.get_logger().warning(f'Cannot open {self.port}: {exc}')

    def poll_serial(self):
        """타이머 콜백: 시리얼 바이트를 모아 완성된 줄마다 파싱을 요청한다.

        시리얼 조각이 여러 번에 나뉘어 와도 줄바꿈까지 버퍼링한다. Arduino가
        분리되면 포트를 닫고 잠시 후 다시 연결한다.
        """
        if self.serial_port is None:
            if time.monotonic() >= self.next_connect_attempt:
                self.connect_serial()
            if self.serial_port is None:
                return

        try:
            waiting = self.serial_port.in_waiting
            data = self.serial_port.read(waiting if waiting else 1)
        except serial.SerialException as exc:
            self.get_logger().warning(f'MQ-3 serial connection lost: {exc}')
            self.close_serial()
            self.next_connect_attempt = time.monotonic() + 2.0
            return

        if not data:
            return

        self.rx_buffer.extend(data)
        if len(self.rx_buffer) > 512:
            self.get_logger().warning('Discarding oversized MQ-3 serial line')
            self.rx_buffer.clear()
            return

        while b'\n' in self.rx_buffer:
            line, _, remaining = self.rx_buffer.partition(b'\n')
            self.rx_buffer = bytearray(remaining)
            self.publish_reading(line.decode('ascii', errors='ignore').strip())

    def publish_reading(self, line):
        """`MQ3,순번,ADC` 한 줄을 검증하고 해당 ROS 토픽에 발행한다.

        순번은 메시지 형식 확인에만 사용한다. ADC는 raw 토픽과 설정된 기준
        전압으로 계산한 voltage 토픽에 발행하고, 보정 구간 안이면 ppm도 발행한다.
        """
        fields = line.split(',')
        if len(fields) != 3 or fields[0] != 'MQ3':
            return

        try:
            int(fields[1])
            adc_value = int(fields[2])
        except ValueError:
            return
        if not 0 <= adc_value <= 1023:
            return

        raw_msg = UInt16()
        raw_msg.data = adc_value
        self.raw_pub.publish(raw_msg)

        voltage_msg = Float32()
        voltage_msg.data = (
            adc_value * self.adc_reference_voltage / 1023.0)
        self.voltage_pub.publish(voltage_msg)

        ethanol_ppm = interpolate_ethanol_ppm(
            adc_value, self.calibration_points)
        if ethanol_ppm is None:
            if self.calibration_points and not self.outside_calibration_range:
                self.get_logger().warning(
                    'MQ-3 ADC is outside the calibrated range; ethanol_ppm '
                    'is not being published')
            self.outside_calibration_range = bool(self.calibration_points)
            return

        if self.outside_calibration_range:
            self.get_logger().info('MQ-3 ADC is back within the calibrated range')
            self.outside_calibration_range = False
        ethanol_msg = Float32()
        ethanol_msg.data = ethanol_ppm
        self.ethanol_pub.publish(ethanol_msg)

    def close_serial(self):
        """열려 있는 Arduino 포트를 닫고 연결 상태를 초기화한다."""
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None

    def destroy_node(self):
        """ROS 노드를 제거하기 전에 시리얼 포트를 정리한다."""
        self.close_serial()
        super().destroy_node()


def main(args=None):
    """브리지 노드를 시작하고 ROS 콜백 처리를 유지한다."""
    rclpy.init(args=args)
    node = MQ3SerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()