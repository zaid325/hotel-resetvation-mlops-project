pipeline {
    agent any

    environment {
        VENV_DIR = "myenv"
        GCP_PROJECT='snappy-striker-475921-q4'
        GCLOUD='/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo 'Cloning GitHub repository into Jenkins...'
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'token acess',  // make sure this matches your Jenkins credentials ID
                            url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git'
                        ]]
                    ])
                }
            }
        }

        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and installing dependencies...'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }
         stage('building and pushing docker image to gcr') {
            steps {
               withCredentials([file(credentialsId : 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                script{
                    echo 'building and pushing docker image to gcr'
                    sh'''
                    export PATH=$PATH:$(GCLOUD_PATH)

                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                    gcloud config set project ${GCP_PROJECT}

                    gcloud auth configure-docker --quite

                    docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                    docker pusht gcr.io/${GCP_PROJECT}/ml-project:latest

                    
                    '''
                }
               }
            }
        }
    }
}



