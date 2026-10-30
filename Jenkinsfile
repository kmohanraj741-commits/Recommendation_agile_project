
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-recommendation'
        KUBECONFIG_CREDENTIALS = 'recommendation-kubeconfig'
        IMAGE_REPOSITORY = 'recommendation-system'
        DOCKER = '"C:\\Users\\Mohan Raj\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe"'
    }

    stages {
        stage('Checkout Verification') {
            steps {
                checkout scm
                bat 'git status --short'
                bat 'git log -1 --oneline'
            }
        }

        stage('Select Version and Validate') {
            steps {
                script {
                    def job = env.JOB_BASE_NAME.toLowerCase()

                    if (job.endsWith('v1')) {
                        env.VERSION = 'v1'
                        env.DEPLOYMENT_NAME = 'recommendation-v1'
                    } else if (job.endsWith('v2')) {
                        env.VERSION = 'v2'
                        env.DEPLOYMENT_NAME = 'recommendation-v2'
                    } else if (job.endsWith('v3')) {
                        env.VERSION = 'v3'
                        env.DEPLOYMENT_NAME = 'recommendation-v3'
                    } else {
                        error('Jenkins job name must end with V1, V2, or V3.')
                    }

                    env.APP_DIR = env.VERSION
                }

                bat 'python -m py_compile %APP_DIR%\\app.py'
            }
        }

        stage('Docker Build and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDENTIALS}",
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat """
                        ${DOCKER} build -t %DOCKERHUB_USER%/%IMAGE_REPOSITORY%:%VERSION% %APP_DIR%
                    """

                    bat """
                        @echo off
                        echo %DOCKERHUB_TOKEN% | ${DOCKER} login -u %DOCKERHUB_USER% --password-stdin
                        if errorlevel 1 exit /b 1

                        ${DOCKER} push %DOCKERHUB_USER%/%IMAGE_REPOSITORY%:%VERSION%
                        if errorlevel 1 exit /b 1

                        ${DOCKER} logout
                    """
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                withCredentials([
                    file(
                        credentialsId: "${KUBECONFIG_CREDENTIALS}",
                        variable: 'KUBECONFIG_FILE'
                    )
                ]) {
                    withCredentials([
                        usernamePassword(
                            credentialsId: "${DOCKERHUB_CREDENTIALS}",
                            usernameVariable: 'DOCKERHUB_USER',
                            passwordVariable: 'DOCKERHUB_TOKEN'
                        )
                    ]) {
                        bat """
                            @echo off
                            set KUBECONFIG=%KUBECONFIG_FILE%

                            kubectl apply -f %APP_DIR%\\k8s-deployment.yaml
                            if errorlevel 1 exit /b 1

                            kubectl set image deployment/%DEPLOYMENT_NAME% %DEPLOYMENT_NAME%=%DOCKERHUB_USER%/%IMAGE_REPOSITORY%:%VERSION%
                            if errorlevel 1 exit /b 1

                            kubectl rollout status deployment/%DEPLOYMENT_NAME% --timeout=120s
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Recommendation System pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check Console Output for the first error.'
        }
    }
}
