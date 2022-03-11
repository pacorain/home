pipeline {
    agent none

    stages { 
        stage('Test') {
            agent {
                docker {
                    image 'ghcr.io/home-assistant/home-assistant:stable'
                    customWorkspace "/home/austin/build/hass/${GIT_BRANCH}"
                    args "-v /home/austin/build/hass/${GIT_BRANCH}:/config"
                }
            }
            steps {
                sh 'hass --script check-config'
            }
          }
      
        stage('Deploy') {
            agent any
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