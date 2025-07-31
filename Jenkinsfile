// Jenkinsfile (CI/CD 파이프라인)
// 이 파일은 GitHub 저장소에 위치하여 Pipeline as Code 원칙을 따릅니다.
pipeline {
    // Jenkins 컨트롤러(my-jenkins-lts 이미지로 실행 중인) 자체에서 파이프라인 단계를 실행
    agent any

    // 전역 환경 변수 정의
    environment {
        // 호스트의 Docker 데몬 소켓 경로. Jenkins 컨테이너 내부의 Docker CLI가 데몬과 통신하는 데 사용.
        DOCKER_HOST_SOCKET = '/var/run/docker.sock'
        // Docker Hub 사용자명. 여기에 실제 당신의 Docker Hub 사용자명을 입력하세요.
        DOCKER_HUB_USERNAME = 'KwonyunGi73' // <<------ 여기에 당신의 실제 Docker Hub 사용자명 입력!
        // 이 프로젝트에서 빌드될 애플리케이션 Docker 이미지의 이름
        APP_IMAGE_NAME = 'my-python-app' // 원하는 애플리케이션 이미지 이름 설정 가능
    }

    // 파이프라인의 주요 단계들 정의
    stages {
        stage('Checkout Code') {
            steps {
                echo '=== Checking out code from Git ==='
                // GitHub 저장소에서 최신 코드 가져오기
                git url: 'https://github.com/KwonyunGi73/CI-CD-test-project.git', // <<---- 당신의 새 GitHub 저장소 URL
                    branch: 'main' // 당신의 기본 브랜치 이름 (main 또는 master)
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '=== Running Unit Tests ==='
                script {
                    // Docker 데몬 소켓 파일의 권한을 666으로 변경하여 모든 사용자에게 읽기/쓰기 권한 부여
                    // 이는 Jenkins 컨테이너 내부의 'jenkins' 사용자가 docker.sock에 접근할 수 있도록 하는 핵심 권한 설정입니다.
                    // sh "sudo chmod 666 ${DOCKER_HOST_SOCKET}"

                    // Python 애플리케이션 테스트를 위한 Docker 컨테이너 실행
                    // --rm: 컨테이너 실행 종료 시 자동으로 삭제
                    // -v ${DOCKER_HOST_SOCKET}:${DOCKER_HOST_SOCKET}: 호스트의 docker.sock을 컨테이너 내부로 마운트하여 컨테이너 내에서 Docker 명령 사용 가능
                    // -v \$(pwd):/app: 현재 Jenkins 워크스페이스(코드)를 컨테이너 내부의 /app 디렉토리로 마운트
                    // -w /app: 컨테이너의 작업 디렉토리를 /app으로 설정
                    // -e PYTHONPATH=/app: Python이 /app 디렉토리에서 모듈(app.py, test_app.py)을 찾도록 경로 설정
                    // python:3.9-slim-bullseye: Python 테스트 환경을 위한 Docker 이미지 사용
                    // python3 -m unittest discover -s /app -p 'test_*.py': /app 디렉토리에서 'test_*.py' 패턴의 테스트 파일을 찾아 실행
                    sh "docker run --rm -v ${DOCKER_HOST_SOCKET}:${DOCKER_HOST_SOCKET} -v \$(pwd):/app -w /app -e PYTHONPATH=/app python:3.9-slim-bullseye python3 -m unittest discover -s /app -p 'test_*.py'"
                }
            }
        }

        // --- CI/CD 확장: CD 단계 추가 ---

        stage('Build Application Docker Image') {
            steps {
                echo '=== Building Application Docker Image ==='
                script {
                    // 애플리케이션 코드(app.py, test_app.py)를 포함하는 Docker 이미지 빌드
                    // -t: 이미지 태그 (Docker Hub 사용자명/이미지이름:빌드번호)
                    // -f Dockerfile.app: 빌드에 사용할 Dockerfile (프로젝트 루트에 있는 Dockerfile.app 사용)
                    // .: 현재 디렉토리(Jenkins 워크스페이스)를 빌드 컨텍스트로 사용
                    sh "docker build -t ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:\${BUILD_NUMBER} -f Dockerfile.app ."
                    
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            // Docker Hub 로그인 정보를 Jenkins Credentials Store에서 가져옴
            // Jenkins에 'dockerhub-credentials'라는 ID로 Username with password 타입의 자격증명을 미리 등록해야 합니다.
            environment {
                DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials') // Jenkins Credentials ID
            }
            steps {
                echo '=== Pushing Docker Image to Docker Hub ==='
                script {
                    // Docker Hub 로그인: 비밀번호를 표준 입력으로 전달하여 보안 유지
                    sh "echo \$DOCKER_HUB_CREDENTIALS_PSW | docker login -u \$DOCKER_HUB_CREDENTIALS_USR --password-stdin"
                    // 빌드된 애플리케이션 이미지를 Docker Hub에 푸시
                    sh "docker push ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:\${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy Application Container') {
            steps {
                echo '=== Deploying Application Container ==='
                script {
                    // 배포 전, 기존에 실행 중인 동일한 이름의 컨테이너가 있다면 중지하고 삭제
                    // || true: 컨테이너가 없어도 스크립트가 실패하지 않도록 함 (idempotency)
                    sh "docker stop ${APP_IMAGE_NAME} || true"
                    sh "docker rm ${APP_IMAGE_NAME} || true"

                    // Docker Hub에서 방금 푸시한 최신 이미지를 가져와 컨테이너로 실행
                    // -d: 컨테이너를 백그라운드(detached) 모드로 실행
                    // -p 80:5000: 호스트의 80번 포트를 컨테이너의 5000번 포트(예: Flask/Django 앱 기본 포트)와 연결
                    // --name: 컨테이너에 고유한 이름 부여 (이름이 중복되지 않도록)
                    // python app.py: 컨테이너 시작 시 실행될 명령 (app.py가 웹 서버를 구동한다고 가정)
                    sh "docker run -d -p 80:5000 --name ${APP_IMAGE_NAME} ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:\${BUILD_NUMBER} python app.py"
                }
            }
        }
    }

    // 파이프라인 실행 후 항상 실행되는 블록 (성공/실패 피드백)
    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Unit tests and CD pipeline passed successfully! Code is good.'
        }
        failure {
            echo 'Pipeline failed! Check the build logs.'
        }
    }
}