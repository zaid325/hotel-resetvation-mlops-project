pipeline {
    agent any

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
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'token acess',  // ✅ ensure this matches your Jenkins credential ID
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
                        echo '🚀 Building and pushing Docker image to Google Container Registry...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Authenticate with GCP
                            ${GCLOUD_PATH}/gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            ${GCLOUD_PATH}/gcloud config set project ${GCP_PROJECT}
                            ${GCLOUD_PATH}/gcloud auth configure-docker --quiet

                            # Build Docker image
                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                            # Push Docker image to GCR
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }
    }
}
