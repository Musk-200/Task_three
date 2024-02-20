pipeline {
    agent any
    parameters {
        string(name: 'API_URL', defaultValue: '', description: 'Enter API URL')
        string(name: 'USERNAME', defaultValue: '', description: 'Enter username')
        password(name: 'PASSWORD', defaultValue: '', description: 'Enter password')
    }
    stages {
        stage('Run Python Script') {
            steps {
                script {
                    // Set environment variables
                    withEnv(["API_URL=${params.API_URL}", "USERNAME=${params.USERNAME}", "PASSWORD=${params.PASSWORD}"]) {
                        // Run your Python script
                        sh 'echo "API_URL: $API_URL"'
                        sh 'echo "USERNAME: $USERNAME"'
                        sh 'echo "PASSWORD: $PASSWORD"'
                        sh 'python3 fetch_create.py'
                    }
                }
            }
        }
    }
}