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
        stage("rename-docs-folder") {
            
            steps {
                sh 'task rename-site'
                echo 'docs folder renamed to match the repo structure'
            }
        }
        stage("pack-docs-to-one-artifact-file") {
            
            steps {
                sh 'task tar'
                echo 'docs folder is packed into a single file and is ready to be archived as an artifact'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'docs.tar', onlyIfSuccessful: true
        }
    }
}