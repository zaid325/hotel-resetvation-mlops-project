pipeline {
    agent any

    environment {
        VENV_DIR = "myenv"
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
    }
}



