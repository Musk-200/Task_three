pipeline {
    agent any
    stages {
        stage('Run Python Script') {
            steps {
                script {
                    // Set environment variables
                    withEnv(["API_URL=${params.API_URL}", "USERNAME=${params.USERNAME}", "PASSWORD=${params.PASSWORD}"]) {
                        // Run your Python script
                        sh '
                           echo "API_URL: $API_URL"'
                           echo "USERNAME: $USERNAME"'
                           echo "PASSWORD: $PASSWORD"'
                           python3 fetch_create.py'
                        '
                    }
                }
            }
        }
    }
}