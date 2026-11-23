#!/usr/bin/env python3
"""
ROS 2 bag (컬러·깊이·camera_info·/odom·/tf) → 3D 메시 (Open3D TSDF).
  python3 reconstruct_from_bag.py BAG --every 1 [--best] [--out scene.ply]
  --best = --icp + --edge-filter + --stationary
"""
import argparse
import bisect
import os
import sys

import numpy as np

try:
    import open3d as o3d
except ImportError:
    sys.exit('open3d 가 없습니다:  pip install open3d==0.19.0')
try:
    from rosbags.rosbag2 import Reader
    from rosbags.typesys import Stores, get_typestore
except ImportError:
    sys.exit('rosbags 가 없습니다:  pip install rosbags')

TYPESTORE = get_typestore(Stores.ROS2_HUMBLE)

# base_link → 카메라 광학 좌표 회전
R_BASE_OPTICAL = np.array([[0.0, 0.0, 1.0],
                           [-1.0, 0.0, 0.0],
                           [0.0, -1.0, 0.0]])
# TF 가 없을 때 쓰는 LIMO 컬러 렌즈 위치 (base_link 기준, m)
LIMO_CAM_XYZ = [0.096, -0.015, 0.03]


# ---------------------------------------------------------------- bag 읽기
def stamp_ns(msg):
    return msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec


def list_topics(bag):
    with Reader(bag) as r:
        print(f'bag 길이: {r.duration / 1e9:.1f} 초,  메시지 {r.message_count} 개')
        for c in r.connections:
            print(f'  {c.topic:45s} {c.msgtype:32s} {c.msgcount:6d} 개')


def collect_times(reader, topic):
    conns = [c for c in reader.connections if c.topic == topic]
    if not conns:
        return conns, []
    return conns, [t for _, t, _ in reader.messages(connections=conns)]


def read_selected(reader, conns, wanted_times):
    """bag 수신 시각이 wanted_times 에 있는 메시지만 역직렬화해서 {시각: 메시지} 로."""
    wanted = set(wanted_times)
    out = {}
    for conn, t, raw in reader.messages(connections=conns):
        if t in wanted:
            out[t] = TYPESTORE.deserialize_cdr(raw, conn.msgtype)
    return out


def image_to_numpy(msg):
    enc = msg.encoding.lower()
    h, w = msg.height, msg.width
    buf = np.frombuffer(bytes(msg.data), dtype=np.uint8)
    if enc in ('rgb8', 'bgr8'):
        img = buf.reshape(h, msg.step)[:, :w * 3].reshape(h, w, 3)
        return img[:, :, ::-1].copy() if enc == 'bgr8' else img.copy()
    if enc in ('rgba8', 'bgra8'):
        img = buf.reshape(h, msg.step)[:, :w * 4].reshape(h, w, 4)[:, :, :3]
        return img[:, :, ::-1].copy() if enc == 'bgra8' else img.copy()
    if enc in ('16uc1', 'mono16'):
        return buf.view('<u2' if not msg.is_bigendian else '>u2').reshape(h, msg.step // 2)[:, :w].astype(np.uint16)
    if enc == '32fc1':
        d = buf.view('<f4' if not msg.is_bigendian else '>f4').reshape(h, msg.step // 4)[:, :w]
        d = np.nan_to_num(d, nan=0.0, posinf=0.0, neginf=0.0)
        return (d * 1000.0).astype(np.uint16)         # m → mm
    raise ValueError(f'지원하지 않는 영상 형식: {msg.encoding} (raw 영상 토픽을 녹화하세요)')


def resize_nearest(img, h, w):
    if img.shape[0] == h and img.shape[1] == w:
        return img
    ys = (np.arange(h) * img.shape[0] / h).astype(int)
    xs = (np.arange(w) * img.shape[1] / w).astype(int)
    return img[ys][:, xs]


def pose_matrix(p, q):
    x, y, z, w = q.x, q.y, q.z, q.w
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    T = np.eye(4)
    T[:3, :3], T[:3, 3] = R, (p.x, p.y, p.z)
    return T


def odom_to_matrix(msg):
    return pose_matrix(msg.pose.pose.position, msg.pose.pose.orientation)


def lookup_chain(tf_edges, base, frame):
    """TF 에서 base → frame 변환을 찾는다 (frame 에서 부모를 따라 올라감). 없으면 None."""
    T, cur, seen = np.eye(4), frame.lstrip('/'), set()
    while cur != base:
        if cur in seen or cur not in tf_edges:
            return None
        seen.add(cur)
        parent, T_pc = tf_edges[cur]
        T = T_pc @ T
        cur = parent
    return T


def rot_deg(T):
    return np.degrees(np.arccos(np.clip((np.trace(T[:3, :3]) - 1) / 2, -1, 1)))


def remove_flying_pixels(depth_mm, rel=0.03, abs_mm=20, radius=1):
    """깊이가 주변과 갑자기 달라지는 경계 픽셀, 빈 곳(0) 바로 옆 픽셀을 지운다."""
    d = depth_mm.astype(np.float32)
    valid = d > 0
    H, W = d.shape
    pad = radius
    dp = np.pad(np.where(valid, d, np.nan), pad, constant_values=np.nan)
    hi = np.full_like(d, -np.inf)
    lo = np.full_like(d, np.inf)
    has_hole = np.zeros_like(valid)
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            s = dp[pad + dy:pad + dy + H, pad + dx:pad + dx + W]
            has_hole |= np.isnan(s)
            hi = np.fmax(hi, s)
            lo = np.fmin(lo, s)
    jump = (hi - lo) > np.maximum(abs_mm, rel * d)
    out = depth_mm.copy()
    out[valid & (jump | has_hole)] = 0
    return out


def open3d_self_check():
    """일부 Open3D 버전(0.20 등)에서 TSDF 결과가 비어 나오는 문제가 있어 시작 전에 확인."""
    d = np.full((48, 64), 800, np.uint16)
    c = np.full((48, 64, 3), 128, np.uint8)
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(c), o3d.geometry.Image(d), depth_scale=1000.0, depth_trunc=2.0,
        convert_rgb_to_intensity=False)
    v = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=0.01, sdf_trunc=0.04, color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    v.integrate(rgbd, o3d.camera.PinholeCameraIntrinsic(64, 48, 50, 50, 32, 24), np.eye(4))
    if len(v.extract_point_cloud().points) == 0:
        sys.exit(f'[실패] 지금 Open3D({o3d.__version__})에서 재구성 결과가 비어 나옵니다.\n'
                 '       다음 명령으로 0.19 버전을 설치한 뒤 다시 실행하세요:\n'
                 '       pip install open3d==0.19.0')


class IcpRefiner:
    """frame-to-model point-to-plane ICP. 보정은 바닥 로봇에 맞게 제한:
    제자리 회전(odom 이동 < 2 cm)이면 수평 회전만, 이동했으면 바닥 이동 + 수평 회전."""

    def __init__(self, intr, depth_trunc, T_base_cam, max_trans=0.10, max_rot=8.0, min_fitness=0.35):
        self.intr, self.depth_trunc = intr, depth_trunc
        self.T_base_cam = T_base_cam
        self.max_trans, self.max_rot, self.min_fitness = max_trans, max_rot, min_fitness
        self.model = None
        self.accepted = self.rejected = 0

    def _cloud(self, rgbd):
        pc = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, self.intr)
        pc = pc.voxel_down_sample(0.01)
        pc.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))
        return pc

    def refine(self, rgbd, init_pose, moved=None):
        src = self._cloud(rgbd)
        pose = init_pose
        if self.model is not None and len(src.points) > 200:
            T = init_pose
            fit = 0.0
            for dist, iters in ((0.06, 30), (0.03, 30), (0.015, 20)):
                res = o3d.pipelines.registration.registration_icp(
                    src, self.model, dist, T,
                    o3d.pipelines.registration.TransformationEstimationPointToPlane(),
                    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=iters))
                T, fit = res.transformation, res.fitness
            delta = T @ np.linalg.inv(init_pose)
            planar = moved is None or moved >= 0.02
            base = (init_pose @ np.linalg.inv(self.T_base_cam))[:3, 3]   # 로봇 중심 (world)
            yaw = np.arctan2(delta[1, 0], delta[0, 0])
            Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
            shift = delta[:3, :3] @ base + delta[:3, 3] - base           # 로봇 중심이 움직인 양
            delta = np.eye(4)
            delta[:3, :3] = Rz
            delta[:3, 3] = base - Rz @ base + (np.r_[shift[:2], 0] if planar else 0)
            T = delta @ init_pose
            if (fit >= self.min_fitness and np.linalg.norm(delta[:3, 3]) <= self.max_trans
                    and rot_deg(delta) <= self.max_rot):
                pose = T
                self.accepted += 1
            else:
                self.rejected += 1
        world = o3d.geometry.PointCloud(src).transform(pose)
        self.model = world if self.model is None else (self.model + world)
        self.model = self.model.voxel_down_sample(0.01)
        self.model.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))
        return pose


# ---------------------------------------------------------------- 메인
def main():
    ap = argparse.ArgumentParser(description='ROS 2 bag → 3D 메시 재구성 (Open3D TSDF)')
    ap.add_argument('bag', help='ros2 bag record 로 만든 폴더')
    ap.add_argument('--list', action='store_true', help='bag 안의 토픽만 보여주고 종료')
    ap.add_argument('--color-topic', default='/camera/color/image_raw')
    ap.add_argument('--depth-topic', default='/camera/depth/image_raw')
    ap.add_argument('--info-topic', default='/camera/color/camera_info',
                    help='깊이를 컬러에 맞춰 정렬(depth_registration)했다면 컬러 카메라 정보')
    ap.add_argument('--odom-topic', default='/odom')
    ap.add_argument('--cam-xyz', type=float, nargs=3, default=None, metavar=('X', 'Y', 'Z'),
                    help='base_link 기준 카메라 위치 [m]. 주면 TF 대신 이 값을 씀 '
                         f'(기본: TF, 없으면 LIMO 값 {LIMO_CAM_XYZ})')
    ap.add_argument('--cam-pitch', type=float, default=0.0,
                    help='TF 를 못 찾았거나 --cam-xyz 를 줄 때, 카메라가 아래로 숙인 각도 [도]')
    ap.add_argument('--base-frame', default='base_link')
    ap.add_argument('--every', type=int, default=3, help='깊이 프레임 N 개마다 1 개 사용 (기본 3)')
    ap.add_argument('--max-frames', type=int, default=0, help='사용할 최대 프레임 수 (0 = 전부)')
    ap.add_argument('--voxel', type=float, default=0.01, help='메시 해상도 [m] (작을수록 정밀, 느림)')
    ap.add_argument('--depth-min', type=float, default=0.3, help='이보다 가까운 깊이는 버림 [m]')
    ap.add_argument('--depth-trunc', type=float, default=2.0, help='이보다 먼 깊이는 버림 [m]')
    ap.add_argument('--max-dt', type=float, default=0.05, help='컬러-깊이 짝 허용 시간차 [s]')
    ap.add_argument('--icp', action='store_true', help='위치 미세 보정 (ICP)')
    ap.add_argument('--edge-filter', action='store_true', help='경계의 떠다니는 점 지우기')
    ap.add_argument('--stationary', action='store_true', help='로봇이 멈춰 있던 프레임만 사용 (/odom 필요)')
    ap.add_argument('--still-speed', type=float, default=0.02, help='멈춤 판정: 이동 속도 [m/s] 이하')
    ap.add_argument('--still-turn', type=float, default=3.0, help='멈춤 판정: 회전 속도 [도/s] 이하')
    ap.add_argument('--best', action='store_true', help='--icp --edge-filter --stationary 모두 켜기')
    ap.add_argument('--max-triangles', type=int, default=100000,
                    help='삼각형이 이보다 많으면 줄임 (RViz 에서 가볍게 보려고, 0 = 줄이지 않음)')
    ap.add_argument('--out', default='scene.ply')
    args = ap.parse_args()
    if args.best:
        args.icp = args.edge_filter = args.stationary = True

    if not os.path.isdir(args.bag):
        sys.exit(f'bag 폴더가 없습니다: {args.bag}')
    if args.list:
        list_topics(args.bag)
        return
    open3d_self_check()

    with Reader(args.bag) as r:
        c_conns, c_times = collect_times(r, args.color_topic)
        d_conns, d_times = collect_times(r, args.depth_topic)
        i_conns, _ = collect_times(r, args.info_topic)
        o_conns, _ = collect_times(r, args.odom_topic)
        missing = [t for t, c in ((args.color_topic, c_conns), (args.depth_topic, d_conns),
                                  (args.info_topic, i_conns)) if not c]
        if missing:
            print('[실패] bag 에 다음 토픽이 없습니다:', ', '.join(missing))
            print('       --list 로 토픽 이름을 확인하고 --color-topic 등으로 지정하세요.')
            list_topics(args.bag)
            sys.exit(1)

        # 깊이 프레임 + 가장 가까운 컬러 짝
        pairs = []
        for k, dt_ in enumerate(d_times):
            if k % args.every:
                continue
            j = bisect.bisect_left(c_times, dt_)
            cands = [c_times[i] for i in (j - 1, j) if 0 <= i < len(c_times)]
            if not cands:
                continue
            pairs.append((dt_, min(cands, key=lambda t: abs(t - dt_))))
        if args.max_frames:
            pairs = pairs[:args.max_frames]

        depths = read_selected(r, d_conns, [p[0] for p in pairs])
        colors = read_selected(r, c_conns, [p[1] for p in pairs])
        info = TYPESTORE.deserialize_cdr(next(r.messages(connections=i_conns))[2], i_conns[0].msgtype)
        odoms = []
        if o_conns:
            for conn, t, raw in r.messages(connections=o_conns):
                m = TYPESTORE.deserialize_cdr(raw, conn.msgtype)
                odoms.append((stamp_ns(m), odom_to_matrix(m)))
            odoms.sort(key=lambda x: x[0])
        # 카메라 장착 TF (/tf_static + /tf)
        tf_edges = {}  # child → (parent, T)
        tf_conns = [c for c in r.connections if c.topic in ('/tf_static', '/tf')]
        for conn, t, raw in (r.messages(connections=tf_conns) if tf_conns else []):
            for tr in TYPESTORE.deserialize_cdr(raw, conn.msgtype).transforms:
                child = tr.child_frame_id.lstrip('/')
                if child == args.base_frame or child in tf_edges:  # odom→base_link 제외
                    continue
                tf_edges[child] = (tr.header.frame_id.lstrip('/'),
                                   pose_matrix(tr.transform.translation, tr.transform.rotation))

    if not odoms:
        sys.exit(f'[실패] bag 에 {args.odom_topic} 가 없습니다. 로봇 노드(/odom)를 켜고 다시 녹화하세요.')
    opts = [n for n, on in (('icp', args.icp), ('edge-filter', args.edge_filter),
                            ('stationary', args.stationary)) if on]
    print(f'사용 프레임 {len(pairs)} 개 (깊이 {len(d_times)} 개 중 {args.every} 개마다 1 개), '
          f'품질 옵션: {", ".join(opts) or "없음"}')

    # 카메라 내부 파라미터
    d0 = image_to_numpy(depths[pairs[0][0]])
    H, W = d0.shape
    sx, sy = W / info.width, H / info.height
    fx, fy, cx, cy = info.k[0] * sx, info.k[4] * sy, info.k[2] * sx, info.k[5] * sy
    intr = o3d.camera.PinholeCameraIntrinsic(W, H, fx, fy, cx, cy)
    print(f'깊이 {W}x{H}, fx={fx:.1f} fy={fy:.1f} cx={cx:.1f} cy={cy:.1f}')
    if (info.width, info.height) != (W, H):
        print('  (카메라 정보 해상도와 깊이 해상도가 달라 비율로 맞췄습니다)')

    # base_link 기준 카메라 자세
    cam_frame = depths[pairs[0][0]].header.frame_id
    T_base_cam = None
    if args.cam_xyz is None:
        T_base_cam = lookup_chain(tf_edges, args.base_frame, cam_frame)
    if T_base_cam is not None:
        fwd = T_base_cam[:3, :3] @ [0, 0, 1]
        pitch = np.degrees(np.arcsin(-fwd[2]))
        print(f'카메라 장착 위치: TF 에서 찾음 ({args.base_frame} → {cam_frame}) '
              f'xyz=({T_base_cam[0, 3]:.3f}, {T_base_cam[1, 3]:.3f}, {T_base_cam[2, 3]:.3f}) m, 아래로 {pitch:.1f}도')
    else:
        xyz = args.cam_xyz if args.cam_xyz is not None else LIMO_CAM_XYZ
        p = np.radians(args.cam_pitch)
        Ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
        T_base_cam = np.eye(4)
        T_base_cam[:3, :3], T_base_cam[:3, 3] = Ry @ R_BASE_OPTICAL, xyz
        why = '직접 지정' if args.cam_xyz is not None else f'TF 에 {args.base_frame} → {cam_frame} 없음, LIMO 기본값'
        print(f'카메라 장착 위치: {why} xyz=({xyz[0]:.3f}, {xyz[1]:.3f}, {xyz[2]:.3f}) m, 아래로 {args.cam_pitch:.1f}도')
    odom_stamps = [o[0] for o in odoms]

    def odom_at(stamp):
        j = bisect.bisect_left(odom_stamps, stamp)
        cands = [i for i in (j - 1, j) if 0 <= i < len(odoms)]
        return odoms[min(cands, key=lambda i: abs(odom_stamps[i] - stamp))][1]

    def is_still(stamp, half=150_000_000):
        a, b = odom_at(stamp - half), odom_at(stamp + half)
        dt = 2 * half / 1e9
        d = np.linalg.inv(a) @ b
        return (np.linalg.norm(d[:3, 3]) / dt <= args.still_speed and rot_deg(d) / dt <= args.still_turn)

    volume = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=args.voxel, sdf_trunc=4 * args.voxel,
        color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    icp = IcpRefiner(intr, args.depth_trunc, T_base_cam) if args.icp else None

    if args.stationary:
        still = [p for p in pairs if is_still(stamp_ns(depths[p[0]]))]
        print(f'멈춰 있던 프레임 {len(still)} 개 / {len(pairs)} 개')
        if len(still) >= 5:
            pairs = still
        else:
            print('  (멈춘 프레임이 5 개보다 적어 전체를 씁니다. 멈췄다 움직이며 찍어 주세요)')

    poses, used = [], 0
    prev_odom = None
    correction = np.eye(4)  # ICP 누적 보정
    skipped_sync = 0
    for dt_, ct in pairs:
        dmsg, cmsg = depths[dt_], colors[ct]
        if abs(stamp_ns(dmsg) - stamp_ns(cmsg)) > args.max_dt * 1e9:
            skipped_sync += 1
            continue
        depth = image_to_numpy(dmsg)
        depth[depth < args.depth_min * 1000] = 0
        raw_depth = depth                       # ICP 는 원본 깊이로 (경계 점도 위치 맞추기에 도움)
        if args.edge_filter:
            depth = remove_flying_pixels(depth)
        color = resize_nearest(image_to_numpy(cmsg), H, W)
        o3d_color, o3d_depth = o3d.geometry.Image(np.ascontiguousarray(color)), o3d.geometry.Image(depth)
        rgbd_col = o3d.geometry.RGBDImage.create_from_color_and_depth(
            o3d_color, o3d_depth, depth_scale=1000.0, depth_trunc=args.depth_trunc,
            convert_rgb_to_intensity=False)

        cur_odom = odom_at(stamp_ns(dmsg)) @ T_base_cam
        pose = correction @ cur_odom

        if icp is not None:
            moved = None   # 로봇 중심(base_link)이 직전 프레임 대비 움직인 거리
            if prev_odom is not None:
                Tbc_inv = np.linalg.inv(T_base_cam)
                moved = np.linalg.norm((cur_odom @ Tbc_inv)[:3, 3] - (prev_odom @ Tbc_inv)[:3, 3])
            rgbd_icp = rgbd_col if raw_depth is depth else o3d.geometry.RGBDImage.create_from_color_and_depth(
                o3d_color, o3d.geometry.Image(raw_depth), depth_scale=1000.0, depth_trunc=args.depth_trunc,
                convert_rgb_to_intensity=False)
            pose = icp.refine(rgbd_icp, pose, moved)
            correction = pose @ np.linalg.inv(cur_odom)

        volume.integrate(rgbd_col, intr, np.linalg.inv(pose))
        poses.append(pose)
        prev_odom = cur_odom
        used += 1
        if used % 10 == 0:
            print(f'  {used} 프레임 합침...')

    print(f'합친 프레임 {used} 개  (시간 안 맞아 버림 {skipped_sync})')
    if icp is not None:
        print(f'ICP 보정: 적용 {icp.accepted} 번, 너무 크거나 안 맞아 버림 {icp.rejected} 번')
    if used < 3:
        sys.exit('[실패] 합친 프레임이 너무 적습니다. --max-dt 를 늘리거나 --every 를 줄여 보세요.')

    mesh = volume.extract_triangle_mesh()
    mesh.compute_vertex_normals()
    # 작은 조각 제거
    tri_clusters, cluster_n, _ = mesh.cluster_connected_triangles()
    tri_clusters, cluster_n = np.asarray(tri_clusters), np.asarray(cluster_n)
    if len(cluster_n):
        mesh.remove_triangles_by_mask(cluster_n[tri_clusters] < max(50, 0.01 * cluster_n.max()))
        mesh.remove_unreferenced_vertices()
    if args.max_triangles and len(mesh.triangles) > args.max_triangles:
        n0 = len(mesh.triangles)
        mesh = mesh.simplify_quadric_decimation(args.max_triangles)
        mesh.compute_vertex_normals()
        print(f'삼각형 {n0} → {len(mesh.triangles)} 개로 줄임 (--max-triangles)')
    cloud = volume.extract_point_cloud()

    base = os.path.splitext(args.out)[0]
    o3d.io.write_triangle_mesh(args.out, mesh)
    o3d.io.write_point_cloud(base + '_cloud.ply', cloud)
    np.savetxt(base + '_poses.txt', np.array([p.reshape(-1) for p in poses]), fmt='%.6f')
    ext = mesh.get_max_bound() - mesh.get_min_bound()
    print(f'\n완료: {args.out}  (꼭짓점 {len(mesh.vertices)}, 삼각형 {len(mesh.triangles)}, '
          f'크기 {ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f} m)')
    print(f'      {base}_cloud.ply, {base}_poses.txt')


if __name__ == '__main__':
    main()
