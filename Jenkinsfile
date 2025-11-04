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
                        userRemoteConfigs: [[
                            credentialsId: 'token acess',  // ✅ check your Jenkins credentials ID spelling
                            url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git'
                        ]]
                    ])
                }
            }
        }

        stage('Verify Python Environment') {
            steps {
                script {
                    echo '⚙️ Checking Python and pip versions...'
                    sh '''
                        python --version
                        pip --version
                    '''
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
    }
}
