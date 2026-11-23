#!/usr/bin/env python3
"""
ROS 2 bag (컬러·깊이·camera_info·/odom·/tf) → 가벼운 3D 메시 (.ply, OpenGL 뷰어용).
  python3 reconstruct_from_bag.py BAG [--out scene.ply] [--gl]
위치 = 바퀴 오도메트리 + ICP 보정, 경계 잡음 제거, 내보내기 전 노이즈 제거.
출력 PLY: binary little-endian, float x y z / uchar red green blue / list uchar uint vertex_indices
"""
import argparse
import bisect
import os
import sys

import numpy as np

try:
    import open3d as o3d
    from rosbags.rosbag2 import Reader
    from rosbags.typesys import Stores, get_typestore
except ImportError as e:
    sys.exit(f'{e.name} 가 없습니다:  pip install open3d==0.19.0 rosbags "numpy<2"')

TS = get_typestore(Stores.ROS2_HUMBLE)
COLOR, DEPTH, INFO, ODOM = ('/camera/color/image_raw', '/camera/depth/image_raw',
                            '/camera/color/camera_info', '/odom')
BASE = 'base_link'
DEPTH_MIN, MAX_DT = 0.3, 0.1          # m, s (컬러-깊이 짝 허용 시간차)
LIMO_CAM_XYZ = [0.096, -0.015, 0.03]  # TF 가 없을 때 쓰는 LIMO 컬러 렌즈 위치 (base_link 기준, m)
R_BASE_OPT = np.array([[0., 0., 1.], [-1., 0., 0.], [0., -1., 0.]])  # base_link → 카메라 광학 좌표
R_ROS_GL = np.array([[0., -1., 0.], [0., 0., 1.], [-1., 0., 0.]])    # ROS(x앞 z위) → OpenGL(y위 -z앞)


def stamp(msg):
    return msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec


def pose(p, q):
    x, y, z, w = q.x, q.y, q.z, q.w
    T = np.eye(4)
    T[:3, :3] = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                 [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                 [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    T[:3, 3] = (p.x, p.y, p.z)
    return T


def rot_deg(T):
    return np.degrees(np.arccos(np.clip((np.trace(T[:3, :3]) - 1) / 2, -1, 1)))


def to_numpy(msg):
    """rgb8 / bgr8 → HxWx3 uint8, 16UC1 / 32FC1 → HxW uint16 (mm)."""
    enc, h, w = msg.encoding.lower(), msg.height, msg.width
    buf = np.frombuffer(bytes(msg.data), np.uint8).reshape(h, msg.step)
    if enc in ('rgb8', 'bgr8'):
        img = buf[:, :w * 3].reshape(h, w, 3)
        return np.ascontiguousarray(img[:, :, ::-1] if enc == 'bgr8' else img)
    if enc == '16uc1':
        return buf[:, :w * 2].copy().view('<u2')
    if enc == '32fc1':
        return (np.nan_to_num(buf[:, :w * 4].copy().view('<f4')) * 1000).astype(np.uint16)
    raise ValueError(f'지원하지 않는 영상 형식: {msg.encoding}')


def remove_flying_pixels(d, rel=0.03, abs_mm=20):
    """깊이가 주변(3x3)과 갑자기 달라지는 경계 픽셀과 빈 곳 바로 옆 픽셀을 지움."""
    f = np.pad(d.astype(np.float32), 1)
    H, W = d.shape
    nb = np.stack([f[1 + dy:1 + dy + H, 1 + dx:1 + dx + W] for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
    bad = (nb == 0).any(0) | (nb.max(0) - nb.min(0) > np.maximum(abs_mm, rel * d))
    out = d.copy()
    out[bad] = 0
    return out


class Icp:
    """frame-to-model point-to-plane ICP. 바닥 로봇에 맞게 보정을 제한:
    제자리 회전(이동 < 2 cm)이면 수평 회전만, 이동했으면 바닥 이동 + 수평 회전."""

    def __init__(self, intr, T_base_cam):
        self.intr, self.T_base_cam, self.model = intr, T_base_cam, None
        self.ok = self.bad = 0

    def refine(self, rgbd, init, moved):
        src = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, self.intr).voxel_down_sample(0.01)
        src.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(10))
        T = init
        if self.model is not None and len(src.points) > 200:
            fit = 0.0
            for dist, it in ((0.06, 30), (0.03, 30), (0.015, 20)):
                r = o3d.pipelines.registration.registration_icp(
                    src, self.model, dist, T, o3d.pipelines.registration.TransformationEstimationPointToPlane(),
                    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=it))
                T, fit = r.transformation, r.fitness
            d = T @ np.linalg.inv(init)
            c = (init @ np.linalg.inv(self.T_base_cam))[:3, 3]     # 로봇 중심 (world)
            yaw = np.arctan2(d[1, 0], d[0, 0])
            Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
            shift = d[:3, :3] @ c + d[:3, 3] - c                     # 로봇 중심이 움직인 양
            d = np.eye(4)
            d[:3, :3] = Rz
            d[:3, 3] = c - Rz @ c + (np.r_[shift[:2], 0] if moved >= 0.02 else 0)
            if fit >= 0.35 and np.linalg.norm(d[:3, 3]) <= 0.10 and rot_deg(d) <= 8.0:
                T = d @ init
                self.ok += 1
            else:                                                     # 너무 크게 틀어지면 odom 그대로
                T = init
                self.bad += 1
        self.model = src.transform(T) if self.model is None else (self.model + src.transform(T))
        self.model = self.model.voxel_down_sample(0.01)
        self.model.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(10))
        return T


def write_ply(path, v, c, f):
    """OpenGL 에서 바로 버퍼로 올릴 수 있는 최소 PLY (법선 없음, c=None 이면 색도 없음)."""
    vert = np.empty(len(v), [('p', '<f4', 3)] + ([('c', 'u1', 3)] if c is not None else []))
    vert['p'] = v
    if c is not None:
        vert['c'] = c
    face = np.empty(len(f), [('n', 'u1'), ('i', '<u4', 3)])
    face['n'], face['i'] = 3, f
    with open(path, 'wb') as fp:
        fp.write((f'ply\nformat binary_little_endian 1.0\nelement vertex {len(v)}\n'
                  'property float x\nproperty float y\nproperty float z\n'
                  + ('property uchar red\nproperty uchar green\nproperty uchar blue\n' if c is not None else '')
                  + f'element face {len(f)}\nproperty list uchar uint vertex_indices\nend_header\n').encode())
        vert.tofile(fp)
        face.tofile(fp)


def main():
    ap = argparse.ArgumentParser(description='ROS 2 bag → 가벼운 3D 메시')
    ap.add_argument('bag')
    ap.add_argument('--out', default='scene.ply')
    ap.add_argument('--gl', action='store_true', help='OpenGL 좌표(y 위)로 바꾸고 가운데·바닥을 원점에 맞춤')
    ap.add_argument('--no-color', action='store_true', help='색 없이 좌표·삼각형만 저장')
    ap.add_argument('--raw', action='store_true', help='보정·잡음 제거 없이 (비교용)')
    ap.add_argument('--voxel', type=float, default=0.01, help='메시 해상도 m')
    ap.add_argument('--depth-trunc', type=float, default=1.5, help='이보다 먼 깊이는 버림 m')
    ap.add_argument('--max-triangles', type=int, default=50000)
    ap.add_argument('--cam-xyz', type=float, nargs=3, help='TF 대신 쓸 카메라 위치 (base_link 기준 m)')
    ap.add_argument('--cam-pitch', type=float, default=0.0, help='--cam-xyz 와 함께: 아래로 숙인 각도 (도)')
    a = ap.parse_args()

    # Open3D 0.20 은 TSDF 결과가 비어 나오는 문제가 있어 먼저 확인
    chk = o3d.pipelines.integration.ScalableTSDFVolume(0.01, 0.04, o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    chk.integrate(o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d.geometry.Image(np.full((48, 64, 3), 128, np.uint8)), o3d.geometry.Image(np.full((48, 64), 800, np.uint16)),
        convert_rgb_to_intensity=False), o3d.camera.PinholeCameraIntrinsic(64, 48, 50, 50, 32, 24), np.eye(4))
    if not chk.extract_point_cloud().has_points():
        sys.exit(f'[실패] Open3D {o3d.__version__} 에서는 결과가 비어 나옵니다:  pip install open3d==0.19.0')

    with Reader(a.bag) as r:
        by = {}
        for c in r.connections:
            by.setdefault(c.topic, []).append(c)
        missing = [t for t in (COLOR, DEPTH, INFO, ODOM) if t not in by]
        if missing:
            sys.exit(f'[실패] bag 에 없는 토픽: {", ".join(missing)}\n       있는 토픽: {", ".join(sorted(by))}')
        if by[DEPTH][0].msgcount > 300:
            sys.exit('[실패] 프레임이 너무 많습니다. 먼저 shrink_bag.py 로 줄이세요.')
        msgs = {t: [(tt, TS.deserialize_cdr(raw, c.msgtype)) for c, tt, raw in r.messages(connections=by[t])]
                for t in (COLOR, DEPTH, INFO, ODOM)}
        tf = {}                                                       # child → (parent, T)
        tfc = by.get('/tf', []) + by.get('/tf_static', [])
        for c, _, raw in (r.messages(connections=tfc) if tfc else []):
            for t in TS.deserialize_cdr(raw, c.msgtype).transforms:
                ch = t.child_frame_id.lstrip('/')
                if ch != BASE and ch not in tf:
                    tf[ch] = (t.header.frame_id.lstrip('/'), pose(t.transform.translation, t.transform.rotation))

    colors, info = msgs[COLOR], msgs[INFO][0][1]
    ctimes = [t for t, _ in colors]
    odoms = sorted((stamp(m), pose(m.pose.pose.position, m.pose.pose.orientation)) for _, m in msgs[ODOM])
    otimes = [t for t, _ in odoms]

    def nearest(times, t):
        j = bisect.bisect_left(times, t)
        return min((i for i in (j - 1, j) if 0 <= i < len(times)), key=lambda i: abs(times[i] - t))

    # 카메라 내부·장착 위치
    H, W = to_numpy(msgs[DEPTH][0][1]).shape
    sx, sy = W / info.width, H / info.height
    intr = o3d.camera.PinholeCameraIntrinsic(W, H, info.k[0] * sx, info.k[4] * sy, info.k[2] * sx, info.k[5] * sy)
    cam = msgs[DEPTH][0][1].header.frame_id.lstrip('/')
    T_bc, cur = (None, cam) if a.cam_xyz else (np.eye(4), cam)
    while T_bc is not None and cur != BASE:                       # TF 를 따라 base_link 까지
        if cur not in tf:
            T_bc = None
            break
        cur, T_pc = tf[cur]
        T_bc = T_pc @ T_bc
    from_tf = T_bc is not None
    if T_bc is None:
        p = np.radians(a.cam_pitch)
        T_bc = np.eye(4)
        T_bc[:3, :3] = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]]) @ R_BASE_OPT
        T_bc[:3, 3] = a.cam_xyz or LIMO_CAM_XYZ
    print(f'프레임 {len(msgs[DEPTH])} 개, 카메라 위치 xyz=({T_bc[0, 3]:.3f}, {T_bc[1, 3]:.3f}, {T_bc[2, 3]:.3f}) m'
          f'{" (TF)" if from_tf else " (기본값)" if not a.cam_xyz else ""}')

    vol = o3d.pipelines.integration.ScalableTSDFVolume(
        a.voxel, 4 * a.voxel, o3d.pipelines.integration.TSDFVolumeColorType.NoColor if a.no_color
        else o3d.pipelines.integration.TSDFVolumeColorType.RGB8)
    icp = None if a.raw else Icp(intr, T_bc)
    T_base_inv = np.linalg.inv(T_bc)
    corr, prev, used = np.eye(4), None, 0
    for _, dm in msgs[DEPTH]:
        cm = colors[nearest(ctimes, stamp(dm))][1]
        if abs(stamp(cm) - stamp(dm)) > MAX_DT * 1e9:
            continue
        raw = to_numpy(dm)
        raw[raw < DEPTH_MIN * 1000] = 0
        depth = raw if a.raw else remove_flying_pixels(raw)
        rgb = to_numpy(cm)
        if rgb.shape[:2] != (H, W):                                   # 해상도가 다르면 깊이에 맞춤
            rgb = np.ascontiguousarray(rgb[np.arange(H) * rgb.shape[0] // H][:, np.arange(W) * rgb.shape[1] // W])
        color = o3d.geometry.Image(rgb)
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color, o3d.geometry.Image(depth), 1000.0, a.depth_trunc, convert_rgb_to_intensity=False)
        odom = odoms[nearest(otimes, stamp(dm))][1] @ T_bc
        T = corr @ odom
        if icp:   # 같은 자리(멈춰 있는 동안)의 다음 프레임은 직전 보정을 그대로 씀 (속도)
            moved = turned = np.inf
            if prev is not None:
                moved = np.linalg.norm((odom @ T_base_inv)[:3, 3] - (prev @ T_base_inv)[:3, 3])
                turned = rot_deg(np.linalg.inv(prev) @ odom)
            if not (moved < 0.005 and turned < 0.5):
                rgbd_icp = o3d.geometry.RGBDImage.create_from_color_and_depth(   # ICP 는 원본 깊이로
                    color, o3d.geometry.Image(raw), 1000.0, a.depth_trunc, convert_rgb_to_intensity=False)
                T = icp.refine(rgbd_icp, T, moved)
                corr = T @ np.linalg.inv(odom)
        vol.integrate(rgbd, intr, np.linalg.inv(T))
        prev, used = odom, used + 1
    if used < 3:
        sys.exit('[실패] 합친 프레임이 3 개보다 적습니다 (컬러·깊이 시간이 안 맞음).')
    print(f'합친 프레임 {used} 개' + (f', ICP 보정 {icp.ok} 번 (버림 {icp.bad})' if icp else ''))

    # 내보내기 전 노이즈 제거: 잘못된 면 정리 → 작은 조각 제거 → 표면 매끄럽게 → 삼각형 줄이기
    m = vol.extract_triangle_mesh()
    m.remove_degenerate_triangles()
    m.remove_duplicated_triangles()
    m.remove_duplicated_vertices()
    m.remove_non_manifold_edges()
    if not a.raw:
        cl, n, _ = m.cluster_connected_triangles()
        n = np.asarray(n)
        m.remove_triangles_by_mask(n[np.asarray(cl)] < max(100, 0.02 * n.max()))
        m.remove_unreferenced_vertices()
        m = m.filter_smooth_taubin(number_of_iterations=5)
    if len(m.triangles) > a.max_triangles:
        m = m.simplify_quadric_decimation(a.max_triangles)
    m.remove_unreferenced_vertices()

    v = np.asarray(m.vertices)
    if a.gl:
        v = (v - [v[:, 0].mean(), v[:, 1].mean(), v[:, 2].min()]) @ R_ROS_GL.T
    c = None if a.no_color else (np.clip(np.asarray(m.vertex_colors), 0, 1) * 255).astype(np.uint8)
    write_ply(a.out, v, c, np.asarray(m.triangles))
    ext = v.max(0) - v.min(0)
    print(f'완료: {a.out}  꼭짓점 {len(v)}, 삼각형 {len(m.triangles)}, {os.path.getsize(a.out) / 1e6:.2f} MB, '
          f'크기 {ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f} m')


if __name__ == '__main__':
    main()
