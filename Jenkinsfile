
pipeline {
  agent any
  environment {
      PATH = "/usr/sbin:$PATH"
  }
  stages {
    stage ('build') {
      steps {
        sh 'chmod 777 ./deployment/deploy.sh'
        echo "PATH is: $PATH"
        sh './deployment/deploy.sh'
      }
    }
  }
}