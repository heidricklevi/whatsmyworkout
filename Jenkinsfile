
pipeline {
  agent any
  stages {
    stage ('build') {
      steps {
        sh 'chmod 777 ./deploy/deploy.sh'
        echo "PATH is: $PATH"
        sh './deploy/deploy.sh'
      }
    }
  }
}