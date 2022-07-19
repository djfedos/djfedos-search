pipeline {

    agent any

    stages {

        stage("build-docs") {
            
            steps {
                sh 'pip install mkdocs mkdocs-material'
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

    post {
        always {
            archiveArtifacts artifacts: '/var/jenkins_home/workspace/test-pipeline/docs/site/*', onlyIfSuccessful: true
        }
    }
}