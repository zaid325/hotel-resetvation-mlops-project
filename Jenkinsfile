pipeline {
    agent any

    enviroment{
        VENV_DIR = "myenv"
    }

    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo 'Cloning GitHub repository into Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'token acess', url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git']])
            }
        }
    }
     stage('setting up our virtual envoirment and installing our dependencies') {
            steps {
                script {
                    echo 'setting up our virtual envoirment and installing dependecies'
                    sh'''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install upgrade pip
                    pip install -e .
                    '''
            }
        }
    }
}
}


