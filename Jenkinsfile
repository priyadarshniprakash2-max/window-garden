
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading Window Garden source code...'
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                echo 'Installing Python dependencies...'

                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/python -m pip install -r backend/requirements-dev.txt
                '''

                echo 'Running backend tests...'

                sh '''
                    .venv/bin/python -m pytest tests/ -v
                    .venv/bin/python -m compileall -q backend tests
                '''
            }
        }

        stage('Frontend Build') {
            steps {
                echo 'Installing React dependencies...'

                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run build'
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                echo 'Connecting to AWS EC2...'

                sshagent(credentials: ['window-garden-ec2-ssh']) {
                    sh '''
                        set -euo pipefail

                        ssh \
                          -o BatchMode=yes \
                          -o StrictHostKeyChecking=yes \
                          -o UserKnownHostsFile=/var/jenkins_home/.ssh/known_hosts \
                          ubuntu@15.252.164.15 'bash -se' <<'REMOTE'

set -euo pipefail

echo "Updating Window Garden source code..."

cd /home/ubuntu/window-garden
git fetch origin main
git reset --hard origin/main

echo "Building React frontend..."

cd frontend
npm ci
npm run build

echo "Updating backend dependencies..."

cd ../backend
.venv/bin/python -m pip install -r requirements.txt

echo "Restarting FastAPI..."

sudo systemctl restart window-garden
sudo systemctl is-active --quiet window-garden

echo "Checking backend health..."

for attempt in {1..10}; do
    if curl -fsS http://127.0.0.1:8000/api/health; then
        break
    fi

    if [ "$attempt" -eq 10 ]; then
        echo "Backend health check failed!"
        exit 1
    fi

    sleep 3
done

echo "Checking Nginx..."

curl -fsSI http://127.0.0.1/

echo "EC2 deployment successful!"

REMOTE
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Window Garden CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
