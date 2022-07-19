pipeline {

    agent any

    stages {

        stage("build-docs") {
            
            steps {
                echo 'building docs'
                sh 'task build'
            }
        }
        stage("move-built-docs") {
            
            steps {
                echo 'moving built docs to the doc repo'
            }
        }
        stage("push-built-docs") {
            
            steps {
                echo 'pushing the built docs'
            }
        }
    }
}