#!/usr/bin/env python3
"""
메시(.ply)를 RViz 에 단독으로 띄움 (frame: scene_mesh, topic: /scene_mesh).
  python3 show_mesh_rviz.py scene.ply  &&  rviz2 -d scene_mesh.rviz
"""
import sys

import numpy as np

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, TransformStamped
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

FRAME = 'scene_mesh'
PLY_TYPES = {'char': 'i1', 'int8': 'i1', 'uchar': 'u1', 'uint8': 'u1', 'short': 'i2', 'int16': 'i2',
             'ushort': 'u2', 'uint16': 'u2', 'int': 'i4', 'int32': 'i4', 'uint': 'u4', 'uint32': 'u4',
             'float': 'f4', 'float32': 'f4', 'double': 'f8', 'float64': 'f8'}


def read_ply(path):
    """삼각형 PLY 를 읽어 (꼭짓점 Nx3, 색 Nx3 [0~1] 또는 None, 삼각형 Mx3) 반환."""
    with open(path, 'rb') as f:
        if f.readline().strip() != b'ply':
            raise ValueError('PLY 파일이 아닙니다')
        fmt, elems = None, []
        while True:
            line = f.readline().decode('ascii', 'ignore').strip()
            if line == 'end_header':
                break
            p = line.split()
            if not p:
                continue
            if p[0] == 'format':
                fmt = p[1]
            elif p[0] == 'element':
                elems.append({'name': p[1], 'count': int(p[2]), 'props': []})
            elif p[0] == 'property':
                elems[-1]['props'].append(('list', p[2], p[3], p[4]) if p[1] == 'list' else (p[1], p[2]))
        body = f.read()

    end = '<' if fmt == 'binary_little_endian' else '>'
    data, off = {}, 0
    if fmt == 'ascii':
        tokens = iter(body.split())
    for e in elems:
        if fmt == 'ascii':
            rows = []
            for _ in range(e['count']):
                row = []
                for pr in e['props']:
                    if pr[0] == 'list':
                        n = int(next(tokens))
                        row.append([float(next(tokens)) for _ in range(n)])
                    else:
                        row.append(float(next(tokens)))
                rows.append(row)
            data[e['name']] = (e['props'], rows)
            continue
        if all(pr[0] != 'list' for pr in e['props']):
            dt = np.dtype([(pr[1], end + PLY_TYPES[pr[0]]) for pr in e['props']])
            arr = np.frombuffer(body, dtype=dt, count=e['count'], offset=off)
            off += dt.itemsize * e['count']
            data[e['name']] = arr
        else:   # 면: 'list uchar int vertex_indices' 이고 전부 삼각형이라고 가정
            pr = e['props'][0]
            cnt_t, idx_t = np.dtype(end + PLY_TYPES[pr[1]]), np.dtype(end + PLY_TYPES[pr[2]])
            dt = np.dtype([('n', cnt_t), ('i', idx_t, (3,))])
            arr = np.frombuffer(body, dtype=dt, count=e['count'], offset=off)
            if e['count'] and not np.all(arr['n'] == 3):
                raise ValueError('삼각형이 아닌 면이 있습니다')
            off += dt.itemsize * e['count']
            data[e['name']] = arr['i']

    v = data['vertex']
    if fmt == 'ascii':
        names = [pr[1] for pr in v[0]]
        va = np.array(v[1], float)
        col = lambda k: va[:, names.index(k)]
        has = lambda k: k in names
        faces = np.array([r[0] for r in data['face'][1]], int)
    else:
        col = lambda k: v[k].astype(float)
        has = lambda k: k in v.dtype.names
        faces = np.asarray(data['face'], int)
    verts = np.stack([col('x'), col('y'), col('z')], 1)
    colors = np.stack([col('red'), col('green'), col('blue')], 1) / 255.0 if has('red') else None
    return verts, colors, faces


class MeshViewer(Node):
    def __init__(self, path):
        super().__init__('scene_mesh_viewer')
        verts, colors, faces = read_ply(path)
        # 화면 가운데 + 바닥을 z=0 으로
        verts = verts - [verts[:, 0].mean(), verts[:, 1].mean(), verts[:, 2].min()]
        ext = verts.max(0) - verts.min(0)
        self.get_logger().info(f'{path}: 꼭짓점 {len(verts)}, 삼각형 {len(faces)}, '
                               f'크기 {ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f} m')

        m = Marker()
        m.header.frame_id = FRAME
        m.ns, m.id, m.type, m.action = 'scene', 0, Marker.TRIANGLE_LIST, Marker.ADD
        m.pose.orientation.w = 1.0
        m.scale.x = m.scale.y = m.scale.z = 1.0
        m.color = ColorRGBA(r=0.8, g=0.8, b=0.8, a=1.0)
        tri = verts[faces.reshape(-1)]
        m.points = [Point(x=float(x), y=float(y), z=float(z)) for x, y, z in tri]
        if colors is not None:
            c = colors[faces.reshape(-1)]
            m.colors = [ColorRGBA(r=float(r), g=float(g), b=float(b), a=1.0) for r, g, b in c]
        self.marker = m

        self.pub = self.create_publisher(Marker, '/scene_mesh', 1)
        self.tf = StaticTransformBroadcaster(self)       # RViz 고정 좌표계로 쓸 수 있게 프레임 하나 등록
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id, t.child_frame_id = 'scene_root', FRAME
        t.transform.rotation.w = 1.0
        self.tf.sendTransform(t)
        self.create_timer(2.0, self.publish)
        self.get_logger().info("RViz: Fixed Frame = 'scene_mesh', Marker 토픽 = /scene_mesh")

    def publish(self):
        self.marker.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(self.marker)


def main():
    if len(sys.argv) < 2:
        sys.exit('사용: python3 show_mesh_rviz.py <메시.ply>')
    rclpy.init()
    node = MeshViewer(sys.argv[1])
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
