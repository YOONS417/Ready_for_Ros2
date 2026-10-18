# Ready_for_Ros2
temporary repository for testing


# 🚀 팀 프로젝트 GitHub 사용 가이드

본 레포지토리는 팀원들이 함께 작업하는 공간입니다. 아래 안내에 따라 환경 설정 및 소스코드 변경 사항을 올려주세요!

---

# 최초 설정 (딱 한 번만 실행)

### 사용자 정보 등록
터미널(Terminal) 또는 Git Bash를 열고 아래 명령어를 입력하여 본인의 정보를 등록합니다.

 git config --global user.name "본인의 GitHub 이름"

 git config --global user.email "본인의 GitHub 이메일"


### 작업할 로컬 폴더로 이동한 후 아래 명령어로 원격 저장소를 내 컴퓨터로 복사

 git clone https://github.com/YOONS417/Ready_for_Ros2.git

 cd Ready_for_Ros2



# 1단계: 최신 코드 불러오기 (작업 시작 전 필수!)
다른 팀원이 올려둔 코드가 있을 수 있으므로 작업 전 항상 최신 상태로 업데이트.                              
 git pull origin main



# 2단계: 변경된 파일 올릴 준비하기 (Git Add)
수정한 파일들을 커밋할 대상으로 등록합니다.
#### 전체 변경 사항 등록
 git add .

#### 또는 특정 파일만 등록시
 git add 파일이름



# 3단계: 변경 사항 기록하기 (Git Commit)
어떤 작업을 했는지 알 수 있도록 메시지와 함께 저장합니다.

 git commit -m "feat: 로그인 기능 추가"



# 4단계: GitHub에 반영하기 (Git Push)
작성한 커밋을 원격 저장소로 올려 팀원들과 공유합니다.

 git push origin main

================================================================================================================

# 팀과제 실행 방법

## 1번 터미널 : webots + RViz 실행
  cd 임시폴더/Ready_for_ros2/webots_ros2_ws
  
  colcon build
  
  source install/local_setup.bash

  cd 임시폴더/Ready_for_ros2/webots_ros2_ws/src/py_bt_ros
  
  ros2 launch webots_ros2_turtlebot robot_launch.py nav:=true

  RViz에서 2D Goal Pose + Tool Properties추가
  
  Topic name에서 /bt/goal_pose로 변경
  

## 2번 터미널 : 카메라 활성화

  ros2 topic echo /TurtleBot3Burger/front_camera/image_color
  

## 3번 터미널 : 변경괴 bt_node 실행

  python3 main.py --config config.yaml
