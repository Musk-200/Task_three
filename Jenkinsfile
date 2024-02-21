pipeline {
    agent any
    stages {
        stage('Run Python Script') {
            steps {
                script {
                    // Set environment variables
                    withEnv(["API_URL=${params.API_URL}", "USERNAME=${params.USERNAME}", "PASSWORD=${params.PASSWORD}"]) {
                        // Run your Python script
                        sh 'python3 fetch_create.py'
                
                    }
                }
            }
        }
    }
}