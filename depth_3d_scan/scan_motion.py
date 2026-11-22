"""
촬영 패턴과 /odom 기반 단계 제어 (ROS 없이 시험 가능).
  ('rel', 거리 m, 회전 도)  : 곡선 이동, 거리 0 이면 제자리 회전
  ('goto', x, y, 방향 도)   : 시작 자세 기준 지점으로 이동 (제자리 회전 필요)
"""
import math


def wrap(a):
    return math.atan2(math.sin(a), math.cos(a))


def make_pattern(name, target_dist=0.9, arc_deg=30.0, arc_step=15.0):
    if name == 'approach':
        return [('rel', 0.12, 15), ('rel', 0.12, -30), ('rel', 0.12, 30), ('rel', 0.12, -15)]
    if name == 'sweep':
        return [('rel', 0, 30), ('rel', 0, -15), ('rel', 0, -15), ('rel', 0, -15), ('rel', 0, -15), ('rel', 0, 30)]
    if name == 'panorama':   # 제자리에서 30도씩 한 바퀴 (방향을 모를 때, 화각 66도라 반씩 겹침)
        return [('rel', 0, 30)] * 11
    if name == 'arc':
        # 물체 = 시작 위치 앞 target_dist, 원 위에서 물체를 바라봄
        R = target_dist
        angs = [-a for a in frange(arc_step, arc_deg, arc_step)] + list(frange(arc_step, arc_deg, arc_step))
        steps = []
        for a in angs:
            th = math.radians(a)
            x, y = R - R * math.cos(th), -R * math.sin(th)
            steps.append(('goto', x, y, a))
        return steps
    raise ValueError(f'모르는 패턴: {name} (approach / sweep / panorama / arc)')


def frange(a, b, s):
    out, v = [], a
    while v <= b + 1e-9:
        out.append(v)
        v += s
    return out


def parse_custom(text):
    """'0.1,15; 0,-30; goto:0.2,0.1,10' 같은 문자열 → 단계 목록."""
    steps = []
    for part in text.split(';'):
        part = part.strip()
        if not part:
            continue
        if part.startswith('goto:'):
            x, y, a = (float(v) for v in part[5:].split(','))
            steps.append(('goto', x, y, a))
        else:
            d, a = (float(v) for v in part.split(','))
            steps.append(('rel', d, a))
    return steps


class StepExecutor:
    """한 단계를 odom 피드백으로 실행. update(x, y, yaw, front) → (v, w, done)."""

    def __init__(self, lin_speed=0.08, ang_speed=0.35, yaw_tol_deg=2.0, pos_tol=0.02,
                 front_stop=0.30, timeout=25.0, allow_in_place=True):
        self.v, self.w = lin_speed, ang_speed
        self.yaw_tol, self.pos_tol = math.radians(yaw_tol_deg), pos_tol
        self.front_stop, self.timeout = front_stop, timeout
        self.allow_in_place = allow_in_place
        self.step = None
        self.result = ''

    def start(self, step, pose, origin, now):
        """origin = 시작 자세 (goto 좌표 기준)."""
        self.step, self.t0 = step, now
        self.p0 = pose
        self.phase = 0
        self.result = ''
        if step[0] == 'rel':
            _, d, a = step
            self.goal_yaw = wrap(pose[2] + math.radians(a))
            self.dist = abs(d)
            self.sign = 1.0 if d >= 0 else -1.0
            self.turn = math.radians(a)
        else:
            _, gx, gy, ga = step
            ox, oy, oyaw = origin
            self.gx = ox + gx * math.cos(oyaw) - gy * math.sin(oyaw)
            self.gy = oy + gx * math.sin(oyaw) + gy * math.cos(oyaw)
            self.goal_yaw = wrap(oyaw + math.radians(ga))

    def _turn_to(self, yaw, target):
        e = wrap(target - yaw)
        if abs(e) <= self.yaw_tol:
            return 0.0, True
        w = max(0.15, min(self.w, 1.5 * abs(e)))
        return math.copysign(w, e), False

    def update(self, x, y, yaw, front, now):
        if now - self.t0 > self.timeout:
            self.result = 'timeout'
            return 0.0, 0.0, True
        if self.step[0] == 'rel':
            if self.dist < 1e-3:  # 제자리 회전
                if not self.allow_in_place:
                    self.result = 'skipped(in-place not allowed)'
                    return 0.0, 0.0, True
                w, ok = self._turn_to(yaw, self.goal_yaw)
                return 0.0, w, ok
            if self.phase == 0:
                moved = math.hypot(x - self.p0[0], y - self.p0[1])
                if self.sign > 0 and front is not None and front < self.front_stop:
                    self.result = f'blocked(front {front:.2f} m)'
                    return 0.0, 0.0, True
                if moved >= self.dist - 1e-3:
                    self.phase = 1
                else:
                    v = self.sign * self.v
                    w = self.turn * self.v / self.dist  # 곡률 일정
                    return v, w, False
            # 남은 방향 보정
            if self.allow_in_place:
                w, ok = self._turn_to(yaw, self.goal_yaw)
                return 0.0, w, ok
            return 0.0, 0.0, True
        # goto: 돌기 → 직진 → 돌기
        if not self.allow_in_place:
            self.result = 'skipped(goto needs in-place turning)'
            return 0.0, 0.0, True
        dist = math.hypot(self.gx - x, self.gy - y)
        if self.phase == 0:
            if dist <= self.pos_tol:
                self.phase = 2
            else:
                w, ok = self._turn_to(yaw, math.atan2(self.gy - y, self.gx - x))
                if not ok:
                    return 0.0, w, False
                self.phase = 1
        if self.phase == 1:
            if dist <= self.pos_tol:
                self.phase = 2
            else:
                if front is not None and front < self.front_stop:
                    self.result = f'blocked(front {front:.2f} m)'
                    return 0.0, 0.0, True
                head = math.atan2(self.gy - y, self.gx - x)
                e = wrap(head - yaw)
                if abs(e) > math.radians(25):  # 많이 틀어지면 다시 돌기
                    self.phase = 0
                    return 0.0, 0.0, False
                v = min(self.v, max(0.03, 1.2 * dist))
                return v, 1.5 * e, False
        w, ok = self._turn_to(yaw, self.goal_yaw)
        return 0.0, w, ok
