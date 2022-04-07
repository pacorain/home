pipeline {
    agent {label 'local'}

    stages { 
        stage('Test HASS config') {
            steps {
                sh 'cp fake_secrets.yaml secrets.yaml'
                sh 'touch groups.yaml automations.yaml scenes.yaml scripts.yaml'
                sh 'docker run --rm -v ${PWD}:/config ghcr.io/home-assistant/home-assistant:stable hass --script check_config -c /config'
            }
          }
      
        stage('Deploy HASS config') {
            when {
              branch 'main'
            }
            steps {
                withCredentials([
                  string(credentialsId: 'homeAssistantHost', variable: 'HOME_ASSISTANT_HOST'), 
                  sshUserPrivateKey(credentialsId: 'homeAssistantDeploy', usernameVariable: 'HOME_ASSISTANT_USERNAME', keyFileVariable: 'HOME_ASSISTANT_DEPLOY_KEY')
                ]) {
                  sh '''
                    ssh -i $HOME_ASSISTANT_DEPLOY_KEY -l $HOME_ASSISTANT_USERNAME $HOME_ASSISTANT_HOST "sudo bash -c 'git -C /config pull && source /etc/profile.d/homeassistant.sh && ha core restart;'"
                  '''
                }
            }
        }
    }

    post {
      always {
        script {
          if (env.BRANCH_NAME == 'main') {
            withCredentials([string(credentialsId: 'discordWebhookSmarthome', variable: 'DISCORD_WEBHOOK_SMARTHOME')]) {
              discordSend description: ${sh(returnStdout:true, script: "git log --format=format:%s -1 ${GIT_COMMIT}")}, link: "https://github.com/pacorain/home/commit/${env.GIT_COMMIT}", result: currentBuild.currentResult, title: env.JOB_NAME, webhookURL: env.DISCORD_WEBHOOK_SMARTHOME
            }
          }
        }
      }
    }
}