#!/usr/bin/env python3
"""
재구성에 필요한 프레임만 남겨 bag 축소 (zstd 압축).
  python3 shrink_bag.py SRC DST [--frames 40] [--stationary] [--no-compress]
"""
import argparse
import bisect
import math
import os
import sys

try:
    from rosbags.rosbag2 import CompressionFormat, CompressionMode, Reader, Writer
    from rosbags.typesys import Stores, get_typestore
except ImportError:
    sys.exit('rosbags 가 없습니다:  pip install rosbags')

COLOR, DEPTH, ODOM = '/camera/color/image_raw', '/camera/depth/image_raw', '/odom'
IMAGE_TYPES = ('sensor_msgs/msg/Image', 'sensor_msgs/msg/CompressedImage', 'sensor_msgs/msg/PointCloud2')
TS = get_typestore(Stores.ROS2_HUMBLE)

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('dst')
ap.add_argument('--frames', type=int, default=30, help='남길 깊이 프레임 수')
ap.add_argument('--stationary', action='store_true', help='로봇이 멈춰 있던 프레임 중에서 고름')
ap.add_argument('--no-compress', action='store_true')
args = ap.parse_args()
if os.path.exists(args.dst):
    sys.exit(f'{args.dst} 가 이미 있습니다.')


def nearest(ts, t):
    j = bisect.bisect_left(ts, t)
    return min((i for i in (j - 1, j) if 0 <= i < len(ts)), key=lambda i: abs(ts[i] - t), default=None)


with Reader(args.src) as r:
    conns = {}
    for c in r.connections:
        conns.setdefault(c.topic, []).append(c)
    for t in (COLOR, DEPTH):
        if t not in conns:
            sys.exit(f'[실패] {t} 가 bag 에 없습니다. 있는 토픽: {", ".join(sorted(conns))}')
    d_times = [t for _, t, _ in r.messages(connections=conns[DEPTH])]
    c_times = [t for _, t, _ in r.messages(connections=conns[COLOR])]

    if args.stationary and ODOM in conns:     # ±0.15 초 동안 2 cm/s, 3 도/s 이하면 멈춘 것
        od = []
        for c, t, raw in r.messages(connections=conns[ODOM]):
            m = TS.deserialize_cdr(raw, c.msgtype)
            p, q = m.pose.pose.position, m.pose.pose.orientation
            od.append((t, p.x, p.y, math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))))
        ot = [o[0] for o in od]

        def still(t, h=150_000_000):
            a, b = od[nearest(ot, t - h)], od[nearest(ot, t + h)]
            dyaw = abs(math.atan2(math.sin(b[3] - a[3]), math.cos(b[3] - a[3])))
            return math.hypot(b[1] - a[1], b[2] - a[2]) <= 0.006 and math.degrees(dyaw) <= 0.9

        still_d = [t for t in d_times if still(t)]
        print(f'멈춰 있던 깊이 프레임 {len(still_d)} / {len(d_times)}')
        if len(still_d) >= 5:
            d_times = still_d
    elif args.stationary:
        print(f'  ({ODOM} 가 없어 --stationary 를 끕니다)')

    keep_d = set(d_times[::max(1, len(d_times) // args.frames)][:args.frames])
    keep_c = {c_times[i] for i in (nearest(c_times, t) for t in keep_d) if i is not None}

    w = Writer(args.dst, version=8)
    if not args.no_compress:
        w.set_compression(CompressionMode.FILE, CompressionFormat.ZSTD)
    with w:
        out = {}
        for c in r.connections:
            kw = dict(serialization_format=c.ext.serialization_format, offered_qos_profiles=c.ext.offered_qos_profiles)
            if c.msgdef and c.msgdef.data:
                kw.update(msgdef=c.msgdef.data, rihs01=c.digest or None)
            else:                             # Humble bag 은 메시지 정의가 없을 수 있음 → 기본 정의
                kw.update(typestore=TS)
            out[c.id] = w.add_connection(c.topic, c.msgtype, **kw)
        n = 0
        for c, t, raw in r.messages():
            if (c.topic == DEPTH and t not in keep_d) or (c.topic == COLOR and t not in keep_c) \
                    or (c.msgtype in IMAGE_TYPES and c.topic not in (DEPTH, COLOR)):
                continue
            w.write(out[c.id], t, raw)
            n += 1

size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(args.dst) for f in fs)
print(f'완료: {args.dst}  (깊이 {len(keep_d)} 장, 컬러 {len(keep_c)} 장, 메시지 {n} 개, {size / 1e6:.1f} MB)')
