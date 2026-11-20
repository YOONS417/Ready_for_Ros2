import csv
import math
import os
import statistics
import time
from datetime import datetime, timezone

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Empty, UInt16

class SCD41CharacterizationLogger(Node):
    """SCD41 CO2 기준선과 노출 응답을 CSV로 기록한다."""

    def __init__(self):
        super().__init__('scd41_characterization_logger')
        self.declare_parameter('co2_topic', '/gas/scd41/co2')
        self.declare_parameter('odom_topic', '/odom')
        self.declare_parameter('exposure_start_topic', '/gas/characterization/exposure_start')
        self.declare_parameter('exposure_end_topic', '/gas/characterization/exposure_end')
        self.declare_parameter('output_csv', '~/scd41_characterization.csv')
        self.declare_parameter('baseline_duration_sec', 60.0)
        self.declare_parameter('confirm_samples', 2) # SCD41은 주기가 길어 샘플 수를 줄임
        self.declare_parameter('min_trigger_delta', 100.0) # CO2 변동폭을 고려한 기본값

        baseline_duration = float(self.get_parameter('baseline_duration_sec').value)
        self.confirm_samples = int(self.get_parameter('confirm_samples').value)
        self.min_trigger_delta = float(self.get_parameter('min_trigger_delta').value)

        self.run_started = time.monotonic()
        self.baseline_deadline = self.run_started + baseline_duration
        self.baseline_samples = []
        self.baseline_ready = False
        self.baseline_median = None
        self.trigger_threshold = None

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
            'co2_ppm', 'odom_x', 'odom_y', 'baseline_median'
        ])
        self.csv_writer.writeheader()

        self.co2_sub = self.create_subscription(UInt16, self.get_parameter('co2_topic').value, self.co2_cb, 10)
        self.odom_sub = self.create_subscription(Odometry, self.get_parameter('odom_topic').value, self.odom_cb, 10)
        self.start_sub = self.create_subscription(Empty, self.get_parameter('exposure_start_topic').value, self.start_cb, 10)
        self.end_sub = self.create_subscription(Empty, self.get_parameter('exposure_end_topic').value, self.end_cb, 10)

        self.get_logger().info(f'Recording SCD41 baseline for {baseline_duration}s...')

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
            self.baseline_samples.append(co2_val)
            if now >= self.baseline_deadline:
                self.baseline_median = statistics.median(self.baseline_samples)
                self.trigger_threshold = self.baseline_median + self.min_trigger_delta
                self.baseline_ready = True
                self.get_logger().info(f'Baseline set: {self.baseline_median} ppm')

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
            'baseline_median': self.baseline_median if self.baseline_median else ''
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
