#!/usr/bin/env python3
"""
재구성에 필요한 프레임만 남겨 bag 축소 (zstd 압축).
  python3 shrink_bag.py SRC DST [--frames 40] [--stationary]
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
TYPESTORE = get_typestore(Stores.ROS2_HUMBLE)

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('dst')
ap.add_argument('--frames', type=int, default=30, help='남길 깊이 프레임 수 (기본 30)')
ap.add_argument('--color-topic', default='/camera/color/image_raw')
ap.add_argument('--depth-topic', default='/camera/depth/image_raw')
ap.add_argument('--odom-topic', default='/odom')
ap.add_argument('--stationary', action='store_true',
                help='로봇이 멈춰 있던(/odom 기준) 깊이 프레임 중에서 고름')
ap.add_argument('--no-compress', action='store_true')
args = ap.parse_args()

if os.path.exists(args.dst):
    sys.exit(f'{args.dst} 가 이미 있습니다. 다른 이름을 쓰거나 지우세요.')

with Reader(args.src) as r:
    by_topic = {}
    for c in r.connections:
        by_topic.setdefault(c.topic, []).append(c)
    for t in (args.color_topic, args.depth_topic):
        if t not in by_topic:
            sys.exit(f'[실패] {t} 토픽이 bag 에 없습니다. 있는 토픽: {", ".join(sorted(by_topic))}')

    d_times = [t for _, t, _ in r.messages(connections=by_topic[args.depth_topic])]
    c_times = [t for _, t, _ in r.messages(connections=by_topic[args.color_topic])]
    if args.stationary:
        if args.odom_topic not in by_topic:
            print(f'  ({args.odom_topic} 가 없어 --stationary 를 끕니다)')
        else:
            od = []                                  # (bag 시각, x, y, yaw)
            for conn, t, raw in r.messages(connections=by_topic[args.odom_topic]):
                m = TYPESTORE.deserialize_cdr(raw, conn.msgtype)
                p, q = m.pose.pose.position, m.pose.pose.orientation
                od.append((t, p.x, p.y, math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))))
            ot = [o[0] for o in od]

            def at(t):
                j = bisect.bisect_left(ot, t)
                return od[min((i for i in (j - 1, j) if 0 <= i < len(od)), key=lambda i: abs(ot[i] - t))]

            def still(t, half=150_000_000):
                a, b = at(t - half), at(t + half)
                dt = 2 * half / 1e9
                dyaw = abs(math.atan2(math.sin(b[3] - a[3]), math.cos(b[3] - a[3])))
                return (math.hypot(b[1] - a[1], b[2] - a[2]) / dt <= 0.02
                        and math.degrees(dyaw) / dt <= 3.0)

            still_d = [t for t in d_times if still(t)]
            print(f'멈춰 있던 깊이 프레임 {len(still_d)} 개 / {len(d_times)} 개')
            if len(still_d) >= 5:
                d_times = still_d
            else:
                print('  (멈춘 프레임이 5 개보다 적어 전체에서 고릅니다)')
    step = max(1, len(d_times) // args.frames)
    keep_d = set(d_times[::step][:args.frames])
    keep_c = set()
    for dt in keep_d:
        j = bisect.bisect_left(c_times, dt)
        cands = [c_times[i] for i in (j - 1, j) if 0 <= i < len(c_times)]
        if cands:
            keep_c.add(min(cands, key=lambda t: abs(t - dt)))

    w = Writer(args.dst, version=8)
    if not args.no_compress:
        w.set_compression(CompressionMode.FILE, CompressionFormat.ZSTD)
    with w:
        out_conn = {}
        for c in r.connections:
            kw = dict(serialization_format=c.ext.serialization_format,
                      offered_qos_profiles=c.ext.offered_qos_profiles)
            if c.msgdef and c.msgdef.data:
                kw.update(msgdef=c.msgdef.data, rihs01=c.digest or None)
            else:                            # Humble bag 은 메시지 정의가 없을 수 있음 → 기본 정의 사용
                kw.update(typestore=TYPESTORE)
            out_conn[c.id] = w.add_connection(c.topic, c.msgtype, **kw)
        n = 0
        for c, t, raw in r.messages():
            if c.topic == args.depth_topic and t not in keep_d:
                continue
            if c.topic == args.color_topic and t not in keep_c:
                continue
            if c.msgtype in ('sensor_msgs/msg/Image', 'sensor_msgs/msg/CompressedImage', 'sensor_msgs/msg/PointCloud2') \
                    and c.topic not in (args.depth_topic, args.color_topic):
                continue                     # 다른 영상·점구름 토픽은 버림
            w.write(out_conn[c.id], t, raw)
            n += 1

size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(args.dst) for f in fs)
print(f'완료: {args.dst}  (깊이 {len(keep_d)} 장, 컬러 {len(keep_c)} 장, 메시지 {n} 개, {size / 1e6:.1f} MB)')
