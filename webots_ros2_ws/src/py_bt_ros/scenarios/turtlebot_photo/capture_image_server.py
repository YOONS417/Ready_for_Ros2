#!/usr/bin/env python3
"""
사진 촬영 서비스 노드.

  - 구독: /TurtleBot3Burger/front_camera/image_color  (sensor_msgs/Image)
  - 서비스: /capture_image  (std_srvs/Trigger)
      요청이 오면 '가장 최근 프레임'을 PNG 로 저장하고,
      response.message 에 저장 경로를 담아 돌려준다.

실행:
    python3 scenarios/turtlebot_photo/capture_image_server.py
    python3 scenarios/turtlebot_photo/capture_image_server.py --ros-args -p out_dir:=/home/jiyoon/bt_photos
"""
import os
import struct
import time
import zlib
from datetime import datetime

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger


def image_msg_to_rgb(msg: Image) -> np.ndarray:
    """sensor_msgs/Image -> (H, W, 3) uint8 RGB. (cv_bridge 없이 변환)"""
    channels = {'bgra8': 4, 'rgba8': 4, 'bgr8': 3, 'rgb8': 3, 'mono8': 1}.get(msg.encoding)
    if channels is None:
        raise ValueError(f'지원하지 않는 인코딩: {msg.encoding}')
    h, w = msg.height, msg.width
    row = np.frombuffer(bytes(msg.data), dtype=np.uint8).reshape(h, msg.step)
    arr = row[:, : w * channels].reshape(h, w, channels)
    if msg.encoding == 'bgra8':
        return arr[:, :, [2, 1, 0]]
    if msg.encoding == 'rgba8':
        return arr[:, :, :3]
    if msg.encoding == 'bgr8':
        return arr[:, :, ::-1]
    if msg.encoding == 'rgb8':
        return arr
    return np.repeat(arr, 3, axis=2)          # mono8


def write_png(path: str, rgb: np.ndarray) -> None:
    """(H, W, 3) uint8 배열을 PNG 로 저장. (OpenCV/PIL 없이 표준 라이브러리만 사용)"""
    h, w, _ = rgb.shape
    raw = b''.join(b'\x00' + rgb[y].tobytes() for y in range(h))

    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 6))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


class CaptureImageServer(Node):
    def __init__(self):
        super().__init__('capture_image_server')
        self.declare_parameter('image_topic', '/TurtleBot3Burger/front_camera/image_color')
        self.declare_parameter('service_name', '/capture_image')
        self.declare_parameter('out_dir', os.path.expanduser('~/bt_photos'))

        topic = self.get_parameter('image_topic').value
        self.out_dir = self.get_parameter('out_dir').value
        os.makedirs(self.out_dir, exist_ok=True)

        self._last = None
        self.create_subscription(Image, topic, self._on_image, qos_profile_sensor_data)
        self.create_service(Trigger, self.get_parameter('service_name').value, self._on_capture)
        self.get_logger().info(f'이미지 구독: {topic} | 저장 폴더: {self.out_dir}')

    def _on_image(self, msg: Image):
        self._last = msg

    def _on_capture(self, request, response):
        if self._last is None:
            response.success = False
            response.message = '아직 카메라 프레임을 받지 못했습니다'
            return response
        try:
            rgb = image_msg_to_rgb(self._last)
            name = datetime.now().strftime('capture_%Y%m%d_%H%M%S.png')
            path = os.path.join(self.out_dir, name)
            write_png(path, rgb)
        except Exception as e:           # 변환/저장 실패를 BT 에 FAILURE 로 전달
            response.success = False
            response.message = f'저장 실패: {e}'
            return response
        self.get_logger().info(f'저장: {path}')
        response.success = True
        response.message = path
        return response


def main():
    rclpy.init()
    node = CaptureImageServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
