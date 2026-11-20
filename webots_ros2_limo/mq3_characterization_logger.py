"""MQ-3 기준선, 노출 응답 지연, 회복 지연을 CSV로 기록한다.

입력은 `/gas/mq3/raw_adc`, `/odom`, 수동 노출 시작/종료 Empty 토픽이다.
센서나 주행 명령을 제어하지 않고 관찰값만 기록한다.
"""

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


def calculate_baseline_thresholds(
        samples, min_trigger_delta, trigger_mad_multiplier,
        min_release_delta, release_mad_multiplier, signal_direction):
    """기준 샘플의 median/MAD에서 감지·해제 ADC 기준을 만든다.

    MAD는 한두 번 튄 ADC에 표준편차보다 덜 민감한 잡음 추정치다.
    증가형/감소형 센서 출력을 모두 지원한다.
    """
    if not samples:
        raise ValueError('baseline samples are required')

    baseline = float(statistics.median(samples))
    mad = float(statistics.median(abs(value - baseline) for value in samples))
    robust_noise = 1.4826 * mad
    trigger_delta = max(
        float(min_trigger_delta), trigger_mad_multiplier * robust_noise)
    release_delta = max(
        float(min_release_delta), release_mad_multiplier * robust_noise)

    if signal_direction == 'increasing':
        trigger = min(1023.0, baseline + trigger_delta)
        release = min(1023.0, baseline + release_delta)
    else:
        trigger = max(0.0, baseline - trigger_delta)
        release = max(0.0, baseline - release_delta)
    return baseline, mad, trigger, release


class MQ3CharacterizationLogger(Node):
    """정지 기준선과 수동 표시된 에탄올 노출 응답을 시각·위치와 함께 저장한다."""

    def __init__(self):
        super().__init__('mq3_characterization_logger')
        self.declare_parameter('adc_topic', '/gas/mq3/raw_adc')
        self.declare_parameter('odom_topic', '/odom')
        self.declare_parameter(
            'exposure_start_topic', '/gas/characterization/exposure_start')
        self.declare_parameter(
            'exposure_end_topic', '/gas/characterization/exposure_end')
        self.declare_parameter('output_csv', '~/mq3_characterization.csv')
        self.declare_parameter('baseline_duration_sec', 60.0)
        self.declare_parameter('adc_reference_voltage', 5.0)
        self.declare_parameter('confirm_samples', 3)
        self.declare_parameter('min_trigger_delta', 30.0)
        self.declare_parameter('trigger_mad_multiplier', 6.0)
        self.declare_parameter('min_release_delta', 10.0)
        self.declare_parameter('release_mad_multiplier', 3.0)
        self.declare_parameter('signal_direction', 'increasing')

        baseline_duration = float(
            self.get_parameter('baseline_duration_sec').value)
        self.confirm_samples = int(self.get_parameter('confirm_samples').value)
        self.adc_reference_voltage = float(
            self.get_parameter('adc_reference_voltage').value)
        self.min_trigger_delta = float(
            self.get_parameter('min_trigger_delta').value)
        self.trigger_mad_multiplier = float(
            self.get_parameter('trigger_mad_multiplier').value)
        self.min_release_delta = float(
            self.get_parameter('min_release_delta').value)
        self.release_mad_multiplier = float(
            self.get_parameter('release_mad_multiplier').value)
        self.signal_direction = str(
            self.get_parameter('signal_direction').value)
        if (baseline_duration <= 0.0 or self.confirm_samples < 1
                or self.adc_reference_voltage <= 0.0):
            raise ValueError(
                'baseline duration, confirmation count, and ADC reference '
                'voltage must be positive')
        if self.signal_direction not in ('increasing', 'decreasing'):
            raise ValueError("signal_direction must be 'increasing' or 'decreasing'")
        if min(self.min_trigger_delta, self.min_release_delta,
               self.trigger_mad_multiplier, self.release_mad_multiplier) < 0.0:
            raise ValueError('threshold deltas and MAD multipliers cannot be negative')

        self.run_started = time.monotonic()
        self.baseline_deadline = self.run_started + baseline_duration
        self.baseline_samples = []
        self.baseline_ready = False
        self.baseline_median = None
        self.baseline_mad = None
        self.trigger_threshold = None
        self.release_threshold = None

        self.robot_x = math.nan
        self.robot_y = math.nan
        self.robot_yaw = math.nan
        self.sample_index = 0
        self.exposure_start_time = None
        self.exposure_end_time = None
        self.response_first_crossing_sec = None
        self.response_confirmed_sec = None
        self.recovery_delay_sec = None
        self.above_threshold_times = []
        self.below_release_times = []
        self.exposure_active = False

        output_path = os.path.expanduser(
            str(self.get_parameter('output_csv').value))
        output_directory = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(output_directory, exist_ok=True)
        self.csv_file = open(output_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=[
            'wall_time_utc', 'monotonic_sec', 'sample_index', 'event',
            'phase', 'adc', 'voltage_estimate_v', 'odom_x', 'odom_y',
            'odom_yaw', 'baseline_median_adc', 'baseline_mad_adc',
            'trigger_threshold_adc', 'release_threshold_adc',
            'response_first_crossing_sec', 'response_confirmed_sec',
            'recovery_delay_sec',
        ])
        self.csv_writer.writeheader()
        self.csv_file.flush()

        self.adc_sub = self.create_subscription(
            UInt16, self.get_parameter('adc_topic').value,
            self.adc_cb, 10)
        self.odom_sub = self.create_subscription(
            Odometry, self.get_parameter('odom_topic').value,
            self.odom_cb, 10)
        self.exposure_start_sub = self.create_subscription(
            Empty, self.get_parameter('exposure_start_topic').value,
            self.exposure_start_cb, 10)
        self.exposure_end_sub = self.create_subscription(
            Empty, self.get_parameter('exposure_end_topic').value,
            self.exposure_end_cb, 10)

        self.get_logger().info(
            f'Recording MQ-3 baseline for {baseline_duration:.1f} seconds '
            f'to {output_path}. Keep the robot stationary in clean air.')

    def odom_cb(self, msg):
        """최근 `/odom` 자세를 저장해 다음 ADC 행에 함께 기록한다."""
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        sin_yaw = 2.0 * (q.w * q.z + q.x * q.y)
        cos_yaw = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = math.atan2(sin_yaw, cos_yaw)

    def exposure_start_cb(self, _msg):
        """수동 노출 시작 마커를 기록하고 응답 지연 측정을 시작한다."""
        if not self.baseline_ready:
            self.get_logger().warning(
                'Exposure start ignored: baseline collection is not complete')
            return
        self.exposure_start_time = time.monotonic()
        self.exposure_end_time = None
        self.response_first_crossing_sec = None
        self.response_confirmed_sec = None
        self.recovery_delay_sec = None
        self.above_threshold_times.clear()
        self.below_release_times.clear()
        self.exposure_active = True
        self._write_row(event='exposure_start')
        self.get_logger().info('Exposure start marked; measuring response delay')

    def exposure_end_cb(self, _msg):
        """수동 노출 종료 마커를 기록하고 baseline 회복 지연 측정을 시작한다."""
        if self.exposure_start_time is None or not self.exposure_active:
            self.get_logger().warning(
                'Exposure end ignored: no active exposure was marked')
            return
        self.exposure_end_time = time.monotonic()
        self.exposure_active = False
        self.below_release_times.clear()
        self._write_row(event='exposure_end')
        self.get_logger().info('Exposure end marked; measuring recovery delay')

    def adc_cb(self, msg):
        """각 ADC 샘플의 시각·추정 전압·최근 위치를 CSV에 기록한다."""
        now = time.monotonic()
        adc_value = int(msg.data)
        self.sample_index += 1

        if not self.baseline_ready:
            self.baseline_samples.append(adc_value)
            if now >= self.baseline_deadline:
                self._finish_baseline()

        if self.baseline_ready:
            if self.exposure_active:
                self._update_response_delay(adc_value, now)
            elif (self.exposure_end_time is not None
                  and self.recovery_delay_sec is None):
                self._update_recovery_delay(adc_value, now)

        self._write_row(adc=adc_value)

    def _finish_baseline(self):
        """baseline 구간의 median/MAD와 양방향 threshold를 계산한다."""
        if not self.baseline_samples:
            self.get_logger().error('No ADC samples received during baseline window')
            self.baseline_deadline = time.monotonic() + 1.0
            return

        (self.baseline_median, self.baseline_mad,
         self.trigger_threshold, self.release_threshold) = (
            calculate_baseline_thresholds(
                self.baseline_samples,
                self.min_trigger_delta,
                self.trigger_mad_multiplier,
                self.min_release_delta,
                self.release_mad_multiplier,
                self.signal_direction))
        self.baseline_ready = True
        self._write_row(event='baseline_complete')
        self.get_logger().info(
            f'Baseline ready: n={len(self.baseline_samples)}, '
            f'median={self.baseline_median:.1f}, MAD={self.baseline_mad:.1f}, '
            f'trigger={self.trigger_threshold:.1f}, '
            f'release={self.release_threshold:.1f} ADC')
        if self.baseline_mad > 50.0:
            self.get_logger().warning(
                'Baseline ADC variation is high; stabilize the sensor/power '
                'before using these thresholds')

    def _is_above_trigger(self, adc_value):
        if self.signal_direction == 'increasing':
            return adc_value >= self.trigger_threshold
        return adc_value <= self.trigger_threshold

    def _is_below_release(self, adc_value):
        if self.signal_direction == 'increasing':
            return adc_value <= self.release_threshold
        return adc_value >= self.release_threshold

    def _update_response_delay(self, adc_value, now):
        """확인 샘플 수가 채워지면 최초 crossing 및 확정 응답 지연을 기록한다."""
        if self._is_above_trigger(adc_value):
            self.above_threshold_times.append(now)
            self.above_threshold_times = self.above_threshold_times[-self.confirm_samples:]
            if (self.response_confirmed_sec is None
                    and len(self.above_threshold_times) >= self.confirm_samples):
                self.response_first_crossing_sec = (
                    self.above_threshold_times[0] - self.exposure_start_time)
                self.response_confirmed_sec = now - self.exposure_start_time
                self._write_row(event='response_confirmed')
                self.get_logger().info(
                    f'Response delay: first crossing='
                    f'{self.response_first_crossing_sec:.3f}s, '
                    f'confirmed={self.response_confirmed_sec:.3f}s')
        else:
            self.above_threshold_times.clear()

    def _update_recovery_delay(self, adc_value, now):
        """확인 샘플 수만큼 release 구간에 머물면 회복 지연을 기록한다."""
        if self._is_below_release(adc_value):
            self.below_release_times.append(now)
            self.below_release_times = self.below_release_times[-self.confirm_samples:]
            if (self.recovery_delay_sec is None
                    and len(self.below_release_times) >= self.confirm_samples):
                self.recovery_delay_sec = (
                    self.below_release_times[0] - self.exposure_end_time)
                self._write_row(event='baseline_recovered')
                self.get_logger().info(
                    f'Baseline recovery delay: {self.recovery_delay_sec:.3f}s')
        else:
            self.below_release_times.clear()

    def _write_row(self, adc=None, event='sample'):
        """한 샘플 또는 이벤트를 CSV에 기록하고 즉시 flush한다."""
        monotonic_now = time.monotonic()
        voltage = None
        if adc is not None:
            voltage = (
                float(adc) * self.adc_reference_voltage / 1023.0)
        row = {
            'wall_time_utc': datetime.now(timezone.utc).isoformat(),
            'monotonic_sec': f'{monotonic_now - self.run_started:.6f}',
            'sample_index': self.sample_index,
            'event': event,
            'phase': self._phase_name(),
            'adc': '' if adc is None else adc,
            'voltage_estimate_v': '' if voltage is None else f'{voltage:.4f}',
            'odom_x': '' if math.isnan(self.robot_x) else f'{self.robot_x:.4f}',
            'odom_y': '' if math.isnan(self.robot_y) else f'{self.robot_y:.4f}',
            'odom_yaw': '' if math.isnan(self.robot_yaw) else f'{self.robot_yaw:.6f}',
            'baseline_median_adc': self._format_optional(self.baseline_median),
            'baseline_mad_adc': self._format_optional(self.baseline_mad),
            'trigger_threshold_adc': self._format_optional(self.trigger_threshold),
            'release_threshold_adc': self._format_optional(self.release_threshold),
            'response_first_crossing_sec': self._format_optional(
                self.response_first_crossing_sec),
            'response_confirmed_sec': self._format_optional(
                self.response_confirmed_sec),
            'recovery_delay_sec': self._format_optional(self.recovery_delay_sec),
        }
        self.csv_writer.writerow(row)
        self.csv_file.flush()

    def _phase_name(self):
        if not self.baseline_ready:
            return 'baseline'
        if self.exposure_active:
            return 'exposure'
        if self.exposure_end_time is not None:
            return 'recovery'
        return 'ready'

    @staticmethod
    def _format_optional(value):
        return '' if value is None else f'{value:.6f}'

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MQ3CharacterizationLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()