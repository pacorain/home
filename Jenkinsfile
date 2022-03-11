pipeline {
    agent {label 'local'}

    stages { 
        stage('Test') {
            steps {
                sh 'docker run --rm -v ${PWD}:/config ghcr.io/home-assistant/home-assistant:stable hass --script check_config -c /config'
            }
          }
      
        stage('Deploy') {
            when {
              branch 'main'
            }
            steps {
                withCredentials([
                  string(credentialsId: 'homeAssistantHost', variable: 'HOME_ASSISTANT_HOST'), 
                  sshUserPrivateKey(credentialsId: 'homeAssistantDeploy', usernameVariable: 'HOME_ASSISTANT_USERNAME', keyFileVariable: 'HOME_ASSISTANT_DEPLOY_KEY')
                ]) {
                  sh 'ssh -i $HOME_ASSISTANT_DEPLOY_KEY -l $HOME_ASSISTANT_USERNAME $HOME_ASSISTANT_HOST "sudo git -C /config pull && sudo ha core restart"'
                }
            }
        }
    }
}