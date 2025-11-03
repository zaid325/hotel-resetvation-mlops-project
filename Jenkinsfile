pipeline {
    agent any

    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo 'Cloning GitHub repository into Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'token acess', url: 'https://github.com/zaid325/hotel-resetvation-mlops-project.git']])
            }
        }
    }
}
}


