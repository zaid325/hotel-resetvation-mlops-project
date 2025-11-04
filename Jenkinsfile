stage('Build and Push Docker Image to GCR') {
    steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
            withEnv([
                'DOCKER_HOST=tcp://docker:2376',
                'DOCKER_TLS_VERIFY=1',
                'DOCKER_CERT_PATH=/certs/client'
            ]) {
                script {
                    echo '🚀 Building and pushing Docker image to Google Container Registry...'
                    sh '''
                        # Authenticate with GCP
                        ${GCLOUD_PATH} auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        ${GCLOUD_PATH} config set project ${GCP_PROJECT}
                        ${GCLOUD_PATH} auth configure-docker --quiet

                        # Test Docker connection
                        docker version

                        # Build and push image
                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }
    }
}
