pipeline {
    agent any {
        docker {
            image 'docker:25.0.3-cli' // 도커 CLI 포함된 이미지
            args '-v /var/run/docker.sock:/var/run/docker.sock' // 호스트의 도커 데몬 사용
        }
    }

    environment {
        DOCKER_HOST_SOCKET = '/var/run/docker.sock'
        DOCKER_HUB_USERNAME = 'KwonyunGi73'
        APP_IMAGE_NAME = 'my-python-app'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '=== Checking out code from Git ==='
                git url: 'https://github.com/KwonyunGi73/CI-CD-test-project.git',
                    branch: 'main'
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '=== Running Unit Tests ==='
                sh '''
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        -e PYTHONPATH=/app \
                        python:3.9-slim-bullseye \
                        python3 -m unittest discover -s /app -p 'test_*.py'
                '''
            }
        }

        stage('Build Application Docker Image') {
            steps {
                echo '=== Building Application Docker Image ==='
                sh '''
                    docker build -t ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:${BUILD_NUMBER} -f Dockerfile.app .
                '''
            }
        }

        stage('Push Docker Image to Docker Hub') {
            environment {
                DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
            }
            steps {
                echo '=== Pushing Docker Image to Docker Hub ==='
                sh '''
                    echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin
                    docker push ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Deploy Application Container') {
            steps {
                echo '=== Deploying Application Container ==='
                sh '''
                    docker stop ${APP_IMAGE_NAME} || true
                    docker rm ${APP_IMAGE_NAME} || true
                    docker run -d -p 80:5000 --name ${APP_IMAGE_NAME} ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:${BUILD_NUMBER} python app.py
                '''
            }
        }
    }

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
