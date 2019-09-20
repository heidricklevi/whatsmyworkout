
pipeline {
  agent any
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