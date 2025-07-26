# Dockerfile.app: Python 애플리케이션을 위한 Dockerfile
# CI/CD 파이프라인의 CD 단계에서 빌드될 이미지 정의

# Python 3.9 버전의 경량 이미지를 베이스로 사용
FROM python:3.9-slim-bullseye

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 코드 복사
# (Jenkinsfile의 CD 빌드 스테이지에서 이 Dockerfile.app을 빌드할 때,
#  Jenkins 작업공간에 있는 app.py와 test_app.py가 복사됩니다.)
COPY app.py .
COPY test_app.py .

# 필요하다면, 컨테이너 시작 시 실행될 기본 명령어 정의 (CD 배포 단계에서 활용 가능)
# 현재는 파이썬 테스트 실행이 주요 목적이므로 CMD는 생략하거나 간략하게
# CMD ["python", "app.py"]