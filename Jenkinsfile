pipeline {
    agent any
    environment {
        VENV_DIR = "myenv"
        GCP_PROJECT = "snappy-striker-475921-q4"
        GCLOUD_PATH = "/usr/local/bin/gcloud"
    }

    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo '📥 Cloning GitHub repository into Jenkins...'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'token acess',
                            url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git'
                        ]]
                    ])
                }
            }
        }

        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo '🐍 Setting up virtual environment...'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    withEnv([
                        'DOCKER_HOST=tcp://docker:2376',
                        'DOCKER_TLS_VERIFY=1',
                        'DOCKER_CERT_PATH=/certs/client'
                    ]) {
                        script {
                            sh '''
                                ${GCLOUD_PATH} auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                                ${GCLOUD_PATH} config set project ${GCP_PROJECT}
                                ${GCLOUD_PATH} auth configure-docker --quiet
                                docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                                docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                            '''
                        }
                    }
                }
            }
        }
    }
}
