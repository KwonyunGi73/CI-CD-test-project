pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'kkyg'               // 본인 DockerHub ID
        APP_IMAGE_NAME = 'my-python-app'                  // 이미지 이름
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '=== Checking out code from Git ==='
                git url: 'https://github.com/KwonyunGi73/CI-CD-test-project.git', branch: 'main'
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
            steps {
                echo '=== Pushing Docker Image to Docker Hub ==='
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials', // 🔸 Jenkins에서 만든 Credentials ID (이름 정확히 맞춰야 함)
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_HUB_USERNAME}/${APP_IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
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
            echo '✅ Unit tests and CD pipeline passed successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check the build logs.'
        }
    }
}
