import numpy as np
import time

class GasSourceLocalizationSystem:
    def __init__(self, uncertainty_threshold=0.8, max_iterations=50):
        self.uncertainty_threshold = uncertainty_threshold  # 종료/안정화 판단 기준 불확실성
        self.max_iterations = max_iterations                # 최대 반복 횟수
        self.iteration_count = 0
        
        # 시스템 상태 변수
        self.baseline_co2 = 500.0   # 기본 설정값 (초기화 단계에서 갱신)
        self.baseline_std = 0.0     # 기준값 변동 범위(표준편차)
        self.measurement_history = [] # 측정 데이터 누적 리스트
        self.estimated_sources = []   # 추정된 누출원 후보 기록
        
    def step_1_initialize_baseline(self, baseline_samples):
        """1단계: 센서 초기화 및 기준값 측정"""
        if not baseline_samples:
            print("[Step 1] 경고: 기준 데이터가 비어 있습니다.")
            return
        
        self.baseline_co2 = float(np.mean(baseline_samples))
        self.baseline_std = float(np.std(baseline_samples))
        print(f"[Step 1 완료] 기준 환경 설정 - CO2 평균: {self.baseline_co2:.2f} ppm, 표준편차: {self.baseline_std:.2f}")

    def step_2_collect_data(self, robot_x, robot_y, co2_val, voc_val, temp_val, hum_val):
        """2단계: 센서 데이터 수집 (위치, 시간, 측정값 바인딩)"""
        data_point = {
            'timestamp': time.time(),
            'x': robot_x,
            'y': robot_y,
            'co2': co2_val,
            'voc': voc_val,
            'temp': temp_val,
            'hum': hum_val,
            'reliability': 0.0  # 3단계에서 계산될 신뢰도
        }
        return data_point

    def step_3_preprocess_and_evaluate_reliability(self, recent_window):
        """3단계: 데이터 전처리 및 신뢰도 평가 (Ci 계산)"""
        if not recent_window:
            return 0.5
        
        # 최근 측정값들의 CO2 변동성(분산) 계산 -> 변동이 작을수록 안정적(신뢰도 상승)
        co2_vals = [d['co2'] for d in recent_window]
        variance = np.var(co2_vals)
        stability_score = 1.0 / (1.0 + variance)
        
        # 센서 상태 및 환경 변화 반영 (예: 기준 편차 대비 안정성)
        # 실제 구현에서는 온습도 변화율이나 센서 지연 상태를 함께 반영할 수 있습니다.
        env_factor = 1.0 
        
        # 신뢰도 Ci 산출 (0.0 ~ 1.0 사이 값으로 정규화)
        ci = float(np.clip(stability_score * env_factor, 0.1, 1.0))
        return ci

    def step_4_estimate_source(self):
        """4단계: 누출원 후보 위치 추정 (농도와 신뢰도를 결합한 가중치 기반 추정)"""
        if not self.measurement_history:
            return None, 0.0
        
        positions = np.array([[d['x'], d['y']] for d in self.measurement_history])
        
        # 기준값 이상의 초과 농도 계산 (음수 방지)
        excess_concentrations = np.array([max(0.0, d['co2'] - self.baseline_co2) for d in self.measurement_history])
        reliabilities = np.array([d['reliability'] for d in self.measurement_history])
        
        # 가중치 = (초과 농도) × (측정 신뢰도 Ci)
        weights = excess_concentrations * reliabilities
        total_weight = np.sum(weights)
        
        if total_weight == 0:
            # 유의미한 가중치가 없으면 단순 최대 농도 위치 선택
            max_idx = np.argmax(excess_concentrations)
            estimated_pos = positions[max_idx]
            uncertainty = 2.0  # 높은 불확실성 부여
        else:
            # 신뢰도와 농도가 반영된 가중 평균 위치 계산 (P_source)
            estimated_pos = np.dot(weights, positions) / total_weight
            
            # 불확실성 평가: 추정 위치 주변의 가중 편차(Spread) 계산
            distances = np.linalg.norm(positions - estimated_pos, axis=1)
            uncertainty = float(np.sum(weights * distances) / total_weight)
            
        self.estimated_sources.append(estimated_pos)
        return estimated_pos, uncertainty

    def step_5_decide_next_location(self, current_pose, estimated_source, uncertainty):
        """5단계: 다음 측정 위치 결정 (불확실성에 따른 적응형 이동 제어)"""
        cur_x, cur_y = current_pose
        est_x, est_y = estimated_source
        
        if uncertainty <= self.uncertainty_threshold:
            # 상황 A: 추정 결과가 안정적임 -> 후보 위치로 직접 접근
            print(f"[Step 5 - 안정적 탐색] 불확실성 낮음 ({uncertainty:.2f}). 후보 위치 방향으로 전진합니다.")
            direction = np.array([est_x - cur_x, est_y - cur_y])
            norm = np.linalg.norm(direction)
            if norm > 0:
                direction = direction / norm
            # 이동 보폭 설정 (예: 0.4m 전진)
            next_x = cur_x + direction[0] * 0.4
            next_y = cur_y + direction[1] * 0.4
            strategy = "APPROACH"
        else:
            # 상황 B: 추정 결과가 불확실함 -> 주변 탐색 영역 확장 또는 지그재그 탐색
            print(f"[Step 5 - 불확실성 대응] 불확실성 높음 ({uncertainty:.2f}). 주변 추가 탐색을 수행합니다.")
            # 아직 데이터가 부족하거나 분산이 클 때 탐색 반경을 넓히기 위한 오프셋 적용
            angle = np.random.uniform(0, 2 * np.pi)
            next_x = cur_x + np.cos(angle) * 0.5
            next_y = cur_y + np.sin(angle) * 0.5
            strategy = "EXPLORE_UNCERTAIN"
            
        return (next_x, next_y), strategy

    def check_termination(self, uncertainty):
        """종료 조건 평가"""
        self.iteration_count += 1
        
        is_stable = uncertainty <= self.uncertainty_threshold
        is_max_iter = self.iteration_count >= self.max_iterations
        
        if is_stable:
            print("[종료 조건 만족] 추정 위치가 충분히 수렴하고 안정적입니다.")
            return True
        if is_max_iter:
            print("[종료 조건 만족] 최대 탐색 횟수에 도달했습니다.")
            return True
            
        return False


# ==========================================
# 실행 흐름 예시 (Main 루프 시뮬레이션)
# ==========================================
if __name__ == "__main__":
    localization = GasSourceLocalizationSystem(uncertainty_threshold=0.5, max_iterations=10)
    
    # 1. 센서 초기화 및 기준값 측정 시뮬레이션 (가스 없는 환경 샘플)
    baseline_samples = [495, 502, 498, 501, 504]
    localization.step_1_initialize_baseline(baseline_samples)
    
    # 로봇의 초기 위치
    current_robot_pose = (0.0, 0.0)
    
    # 6. 이동 후 재측정 및 반복 루프
    for i in range(5):
        print(f"\n--- [Iteration {i+1}] 시작 ---")
        
        # (시뮬레이션) 센서 측정값 수입
        # 실제 구현에서는 아두이노 시리얼 통신이나 ROS 토픽(SCD41, SGP40 등) 값을 받음
        simulated_co2 = 520.0 + (i * 25.0)  # 점차 농도가 높아진다고 가정
        simulated_voc = 100.0
        simulated_temp = 24.5
        simulated_hum = 40.0
        
        # 2단계: 데이터 수집
        new_data = localization.step_2_collect_data(
            current_robot_pose[0], current_robot_pose[1], 
            simulated_co2, simulated_voc, simulated_temp, simulated_hum
        )
        
        # 3단계: 전처리 및 신뢰도 평가
        localization.measurement_history.append(new_data)
        recent_window = localization.measurement_history[-3:] # 최근 3개 데이터 기준
        new_data['reliability'] = localization.step_3_preprocess_and_evaluate_reliability(recent_window)
        print(f"측정 위치: {current_robot_pose} | CO2: {simulated_co2} ppm | 신뢰도(Ci): {new_data['reliability']:.2f}")
        
        # 4단계: 누출원 후보 위치 추정
        est_source, uncertainty = localization.step_4_estimate_source()
        print(f"추정된 누출원 후보 위치(P_source): ({est_source[0]:.2f}, {est_source[1]:.2f}) | 불확실성: {uncertainty:.2f}")
        
        # 종료 조건 체크
        if localization.check_termination(uncertainty):
            print(">>> 누출원 탐색 완료 및 종료 <<<")
            break
            
        # 5단계: 다음 측정 위치 결정
        next_pose, strategy = localization.step_5_decide_next_location(current_robot_pose, est_source, uncertainty)
        print(f"다음 이동 위치: {next_pose} (전략: {strategy})")
        
        # 로봇 위치 갱신 (실제 환경에서는 Nav2 액션 호출 후 도달 대기)
        current_robot_pose = next_pose