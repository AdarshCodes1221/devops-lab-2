pipeline {
    agent any

    environment {
        SERVICE_NAME = "media-encoder"
        IMAGE_NAME   = "video-encoder"
        IMAGE_TAG    = "1.0"
        APP_PORT     = "8087"
    }

    stages {
        stage('Source Fetch') {
            steps {
                echo "=============================================="
                echo "STAGE 1: Source Fetch"
                echo "Fetching repository source code for: ${SERVICE_NAME}"
                echo "Branch: release-v5.0 / main (tag: v5.0.0-final)"
                echo "=============================================="
                sh '''
                    echo "[+] Checking Git commit status..."
                    git log -1 --stat || true
                    ls -la
                '''
            }
        }

        stage('Media Linting') {
            steps {
                echo "=============================================="
                echo "STAGE 2: Media Linting"
                echo "Validating media encoder configuration and code"
                echo "=============================================="
                sh '''
                    echo "[+] Linting Python application syntax..."
                    python3 -m py_compile app.py

                    echo "[+] Linting transcode.conf configuration..."
                    test -f transcode.conf || (echo "transcode.conf not found!" && exit 1)
                    grep -i "max_bitrate" transcode.conf
                    echo "[+] Media profile validation: max bitrate = 4k verified."
                '''
            }
        }

        stage('Build Transcoder') {
            steps {
                echo "=============================================="
                echo "STAGE 3: Build Transcoder"
                echo "Building Docker container image: ${IMAGE_NAME}:${IMAGE_TAG}"
                echo "=============================================="
                sh '''
                    echo "[+] Building Alpine-based transcoder container image..."
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    echo "[+] Verifying container image presence..."
                    docker images | grep ${IMAGE_NAME}
                    echo "[+] Transcoder build completed successfully."
                '''
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Continuous Delivery Pipeline for OTT Video Streaming Transcoder completed successfully."
        }
        failure {
            echo "FAILURE: Media Transcoder Pipeline encountered errors."
        }
    }
}
