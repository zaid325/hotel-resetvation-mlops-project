pipeline {
    agent {
        docker {
            image 'python:3.10'  // ✅ Python preinstalled
        }
    }

    environment {
        VENV_DIR = "myenv"
        GCP_PROJECT = "snappy-striker-475921-q4"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo '📥 Cloning GitHub repository into Jenkins...'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            credentialsId: 'token acess',  // ✅ check your Jenkins credentials ID spelling
                            url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git'
                        ]]
                    ])
                }
            }
        }

        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo '🐍 Setting up virtual environment and installing dependencies...'
                    sh '''
                        python -m venv ${VENV_DIR}
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
                    script {
                        echo '🚀 Building and pushing Docker image to GCR...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Authenticate with GCP
                            ${GCLOUD_PATH}/gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            ${GCLOUD_PATH}/gcloud config set project ${GCP_PROJECT}
                            ${GCLOUD_PATH}/gcloud auth configure-docker --quiet

                            # Build and push Docker image
                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }
    }
}
