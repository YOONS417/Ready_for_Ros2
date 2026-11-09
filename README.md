# Autonomous Mapping & Frontier Exploration Node (`auto_explorer.py`)

사전 지도(Map)가 없는 미지의 실내 환경에서 LIMO 로봇이 스스로 빈 공간을 찾아 주행하며 실시간 SLAM 지도를 완성하는 **경량 프론티어 탐색 및 사각지대 순찰 노드**입니다.

---

## 1. 주요 기능 (Key Features)
* **Phase 1 (프론티어 개척):** 실시간 지도(`/map`)에서 미탐색 영역(`-1`)과 빈 공간(`0`)의 경계선(Frontier)을 추출하여 전 구역 지도를 고속으로 완성합니다.
* **Phase 2 (사각지대 커버리지 순찰):** 1차 맵핑 완료 후, 라이다만 스캔하고 로봇이 직접 방문하지 않은 사각지대 좌표를 추출해 100% 방문 점검 및 무한 순찰을 수행합니다.
* **반응형 장애물 회피 및 자가 복구:** 라이다(`/scan`) 기반 전방·측면 장애물 회피 및 코너 끼임 시 자동 후진 탈출(Self-Recovery) 기동을 지원합니다.
* **RViz2 실시간 시각화:** 로봇의 탐색 반경 및 방문 완료 구역을 초록색 마커(`/coverage_markers`)로 실시간 표시합니다.

---

## 2. 입출력 토픽 인터페이스 (ROS 2 Interfaces)

### Subscribed Topics
| 토픽명 (Topic) | 메시지 타입 (Type) | QoS | 설명 |
| :--- | :--- | :--- | :--- |
| `/scan` | `sensor_msgs/msg/LaserScan` | `BEST_EFFORT` | 전방 및 측면 장애물 거리 감지 |
| `/map` | `nav_msgs/msg/OccupancyGrid` | `DEFAULT` | Cartographer SLAM 실시간 격자 지도 |
| `/odom` | `nav_msgs/msg/Odometry` | `DEFAULT` | 로봇의 현재 위치 및 방향(Yaw) 추정 |

### Published Topics
| 토픽명 (Topic) | 메시지 타입 (Type) | 설명 |
| :--- | :--- | :--- |
| `/cmd_vel` | `geometry_msgs/msg/Twist` | 로봇 주행 속도 명령 (`linear.x`, `linear.y`, `angular.z`) |
| `/coverage_markers` | `visualization_msgs/msg/MarkerArray` | 탐색 완료 영역(초록색 원) 및 현재 목표 지점(노란색 구) 시각화 |

---

## 3. 패키지 적용 및 빌드 방법 (Installation)

기존 `webots_ros2_limo` 패키지에 본 노드를 추가하고 실행 명령어를 등록합니다.

### 1) 노드 파일 복사
이 브랜치의 `auto_explorer.py` 파일을 본인의 ROS 2 워크스페이스 패키지 내부 소스 폴더로 복사합니다.
```bash
cp auto_explorer.py ~/webots_ros2_ws/src/webots_ros2_limo/webots_ros2_limo/
