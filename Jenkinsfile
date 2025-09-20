pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "${params.DOCKER_IMAGE ?: 'mlops-app'}"
        IMAGE_TAG = "${params.IMAGE_TAG ?: 'latest'}"
        DOCKER_HUB_USERNAME = credentials('docker-hub-username')
        DOCKER_HUB_PASSWORD = credentials('docker-hub-password')
        ADMIN_EMAIL = credentials('admin-email')
        EMAIL_USERNAME = credentials('email-username')
        EMAIL_PASSWORD = credentials('email-password')
    }
    
    parameters {
        string(name: 'DOCKER_IMAGE', defaultValue: 'mlops-app', description: 'Docker image name')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out code from repository"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                        docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                script {
                    echo "Testing Docker image..."
                    sh """
                        docker run --rm -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:${IMAGE_TAG}
                        sleep 10
                        curl -f http://localhost:5001/health || exit 1
                        docker stop test-container
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing to Docker Hub..."
                    sh """
                        echo ${DOCKER_HUB_PASSWORD} | docker login -u ${DOCKER_HUB_USERNAME} --password-stdin
                        docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:latest
                        docker push ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Deploy to Production') {
            steps {
                script {
                    echo "Deploying to production environment..."
                    sh """
                        # Stop existing container if running
                        docker stop mlops-app-prod || true
                        docker rm mlops-app-prod || true
                        
                        # Run new container
                        docker run -d \
                            --name mlops-app-prod \
                            --restart unless-stopped \
                            -p 5000:5000 \
                            -v /var/lib/mlops/models:/app/models \
                            -v /var/lib/mlops/data:/app/data \
                            ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:${IMAGE_TAG}
                        
                        # Wait for health check
                        sleep 15
                        curl -f http://localhost:5000/health || exit 1
                    """
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "Deployment successful! Sending notification..."
                emailext (
                    subject: "MLOps CI/CD Pipeline - Jenkins Job Completed Successfully",
                    body: """
                    The Jenkins deployment job has completed successfully!
                    
                    Details:
                    - Build Number: ${env.BUILD_NUMBER}
                    - Docker Image: ${DOCKER_HUB_USERNAME}/${DOCKER_IMAGE}:${IMAGE_TAG}
                    - Deployment Time: ${new Date()}
                    - Application URL: http://localhost:5000
                    
                    The application is now running in production.
                    
                    Best regards,
                    MLOps CI/CD Pipeline
                    """,
                    to: "${ADMIN_EMAIL}",
                    from: "${EMAIL_USERNAME}"
                )
            }
        }
        
        failure {
            script {
                echo "Deployment failed! Sending notification..."
                emailext (
                    subject: "MLOps CI/CD Pipeline - Jenkins Job Failed",
                    body: """
                    The Jenkins deployment job has failed!
                    
                    Details:
                    - Build Number: ${env.BUILD_NUMBER}
                    - Docker Image: ${DOCKER_IMAGE}:${IMAGE_TAG}
                    - Failure Time: ${new Date()}
                    
                    Please check the Jenkins logs for more details.
                    
                    Best regards,
                    MLOps CI/CD Pipeline
                    """,
                    to: "${ADMIN_EMAIL}",
                    from: "${EMAIL_USERNAME}"
                )
            }
        }
        
        always {
            script {
                echo "Cleaning up Docker images..."
                sh """
                    docker image prune -f
                    docker container prune -f
                """
            }
        }
    }
}
