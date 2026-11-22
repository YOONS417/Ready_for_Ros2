import csv
import math
import os
import statistics
import time
from datetime import datetime, timezone

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import Empty, Float32MultiArray, UInt16


class SCD41CharacterizationLogger(Node):
    """SCD41 CO2 기준선과 노출 응답을 CSV로 기록하고 계산된 임계값을 발행한다."""

    def __init__(self):
        super().__init__('scd41_characterization_logger')
        self.declare_parameter('co2_topic', '/gas/scd41/co2')
        self.declare_parameter('odom_topic', '/odom')
        self.declare_parameter('threshold_topic', '/gas/scd41/thresholds')
        self.declare_parameter('exposure_start_topic', '/gas/characterization/exposure_start')
        self.declare_parameter('exposure_end_topic', '/gas/characterization/exposure_end')
        self.declare_parameter('output_csv', '~/scd41_characterization.csv')
        self.declare_parameter('baseline_duration_sec', 30.0)
        self.declare_parameter('min_baseline_samples', 5)
        self.declare_parameter('confirm_samples', 2)
        self.declare_parameter('min_trigger_delta', 150.0)  # 기준선 대비 정지 임계 증가폭(ppm)
        self.declare_parameter('release_delta', 50.0)       # 기준선 대비 해제 임계 증가폭(ppm)

        self.baseline_duration = float(self.get_parameter('baseline_duration_sec').value)
        self.min_baseline_samples = int(self.get_parameter('min_baseline_samples').value)
        self.confirm_samples = int(self.get_parameter('confirm_samples').value)
        self.min_trigger_delta = float(self.get_parameter('min_trigger_delta').value)
        self.release_delta = float(self.get_parameter('release_delta').value)

        if not 0.0 <= self.release_delta < self.min_trigger_delta:
            raise ValueError('release_delta must be non-negative and strictly below min_trigger_delta')
        if self.min_baseline_samples < 1:
            raise ValueError('min_baseline_samples must be positive')

        self.run_started = time.monotonic()
        self.baseline_start_time = None
        self.baseline_deadline = None
        self.baseline_samples = []
        self.baseline_ready = False
        self.baseline_median = None
        self.stop_threshold = None
        self.release_threshold = None

        self.robot_x = math.nan
        self.robot_y = math.nan
        self.sample_index = 0
        self.exposure_active = False
        self.exposure_start_time = None

        output_path = os.path.expanduser(str(self.get_parameter('output_csv').value))
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        self.csv_file = open(output_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=[
            'wall_time_utc', 'monotonic_sec', 'sample_index', 'event',
            'co2_ppm', 'odom_x', 'odom_y', 'baseline_median',
            'stop_threshold', 'release_threshold',
        ])
        self.csv_writer.writeheader()

        # auto_explorer가 늦게 실행돼도 마지막 발행 임계값을 받을 수 있도록 TRANSIENT_LOCAL 설정
        threshold_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.threshold_pub = self.create_publisher(
            Float32MultiArray,
            str(self.get_parameter('threshold_topic').value),
            threshold_qos,
        )

        self.co2_sub = self.create_subscription(
            UInt16, self.get_parameter('co2_topic').value, self.co2_cb, 10)
        self.odom_sub = self.create_subscription(
            Odometry, self.get_parameter('odom_topic').value, self.odom_cb, 10)
        self.start_sub = self.create_subscription(
            Empty, self.get_parameter('exposure_start_topic').value, self.start_cb, 10)
        self.end_sub = self.create_subscription(
            Empty, self.get_parameter('exposure_end_topic').value, self.end_cb, 10)

        self.get_logger().info(
            f'SCD41 첫 데이터 대기 중... 수신 시 {self.baseline_duration:.0f}초간 기준선을 측정합니다.'
        )

    def odom_cb(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def start_cb(self, _msg):
        self.exposure_active = True
        self.exposure_start_time = time.monotonic()
        self._write_row(event='exposure_start')

    def end_cb(self, _msg):
        self.exposure_active = False
        self._write_row(event='exposure_end')

    def co2_cb(self, msg):
        now = time.monotonic()
        co2_val = int(msg.data)
        self.sample_index += 1

        if not self.baseline_ready:
            if self.baseline_start_time is None:
                self.baseline_start_time = now
                self.baseline_deadline = now + self.baseline_duration
                self.get_logger().warning(
                    f'>>> SCD41 첫 데이터 수신! {self.baseline_duration:.0f}초간 기준선 측정을 시작합니다. <<<'
                )

            self.baseline_samples.append(co2_val)
            remaining = max(0.0, self.baseline_deadline - now)

            if now >= self.baseline_deadline and len(self.baseline_samples) >= self.min_baseline_samples:
                self.baseline_median = float(statistics.median(self.baseline_samples))
                self.stop_threshold = self.baseline_median + self.min_trigger_delta
                self.release_threshold = self.baseline_median + self.release_delta
                self.baseline_ready = True

                th_msg = Float32MultiArray()
                th_msg.data = [
                    float(self.baseline_median),
                    float(self.stop_threshold),
                    float(self.release_threshold),
                ]
                self.threshold_pub.publish(th_msg)

                self.get_logger().info(
                    f'Baseline 완료: median={self.baseline_median:.1f} ppm | '
                    f'stop={self.stop_threshold:.1f} ppm | '
                    f'release={self.release_threshold:.1f} ppm (토픽 발행 완료)'
                )
                self._write_row(co2=co2_val, event='baseline_ready')
                return

            self.get_logger().info(
                f'Baseline 측정 중... {remaining:.0f}초 남음 '
                f'(샘플 {len(self.baseline_samples)}개, 현재 {co2_val} ppm)'
            )

        self._write_row(co2=co2_val)

    def _write_row(self, co2=None, event='sample'):
        row = {
            'wall_time_utc': datetime.now(timezone.utc).isoformat(),
            'monotonic_sec': time.monotonic() - self.run_started,
            'sample_index': self.sample_index,
            'event': event,
            'co2_ppm': co2 if co2 is not None else '',
            'odom_x': self.robot_x,
            'odom_y': self.robot_y,
            'baseline_median': self.baseline_median if self.baseline_median is not None else '',
            'stop_threshold': self.stop_threshold if self.stop_threshold is not None else '',
            'release_threshold': self.release_threshold if self.release_threshold is not None else '',
        }
        self.csv_writer.writerow(row)
        self.csv_file.flush()

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SCD41CharacterizationLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()