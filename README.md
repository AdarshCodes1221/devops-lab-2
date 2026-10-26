# OTT Media Transcoder — DevOps Lab

Small practice lab for Git release management, Jenkins CI, Docker, Kubernetes, Terraform, and Ansible.

## Prerequisites
Git, Docker Desktop, kubectl connected to a working cluster, Terraform, and Ansible (usually via WSL on Windows). Jenkins must run on an agent with Git, Python 3, and Docker available.

## 1. Git release workflow (PowerShell, from this folder)
Run once in a clean copy of this project:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\git-release.ps1
```

Verify:
```powershell
git branch --all
git log --oneline --decorate --all
git tag --list
```
Expected final tag: `v5.0.0-final`; config: `max_bitrate=4k`.

## 3. Docker build/run/verify
```powershell
docker build -t video-encoder:1.0 .
docker run -d --name video-encoder -p 8087:80 video-encoder:1.0
docker ps --filter name=video-encoder
curl.exe -i http://localhost:8087
docker logs video-encoder
```
Expected HTTP body: `transcoder engine ready`.

Cleanup:
```powershell
docker rm -f video-encoder
```

## 4. Kubernetes (cluster must be running)
The Kubernetes deployment runs the custom `video-encoder:1.0` image built above.

```powershell
kubectl apply -f .\k8s\deployment.yaml
kubectl rollout status deployment/media-encoder
kubectl get deployments,pods,services -l app=media-encoder -o wide
curl.exe -I http://localhost:30097
```
The manifest uses the locally built `video-encoder:1.0` image. Docker Desktop Kubernetes can use
this image directly. For another cluster, push the image to a registry and replace the image
reference before applying. If localhost NodePort is not reachable, use your cluster's node IP
with port `30097`.

## 5. Terraform: generate and verify `terraform/output.end`
```powershell
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform plan
terraform -chdir=terraform apply -auto-approve
terraform -chdir=terraform output -raw transcoder_output_file
Get-Content .\terraform\output.end
```

## 6. Verify with Ansible ad hoc commands
Run these in WSL/Linux with Ansible installed, from the project root:
```bash
ansible localhost -i localhost, -c local -m ansible.builtin.stat -a "path=terraform/output.end"
ansible localhost -i localhost, -c local -m ansible.builtin.command -a "cat terraform/output.end"
```

## 7. Jenkins
Create a Pipeline job in Jenkins and configure it to use this repository and `Jenkinsfile`
(Pipeline script from SCM is preferred). The Jenkins agent must have Git, Python 3, and Docker
CLI/daemon access. Stages: Source Fetch → Media Linting → Build Transcoder.

The local Jenkins instance used for verification is available at `http://localhost:8080`.
After logging in, create or select a Pipeline job, set its SCM URL to
`https://github.com/AdarshCodes1221/devops-lab-2.git`, select branch `main`, set the script path
to `Jenkinsfile`, and select **Build Now**. The equivalent local checks are:

```powershell
python -m py_compile app.py
Select-String -Path transcode.conf -Pattern '^max_bitrate=4k$'
docker build -t video-encoder:1.0 .
```

## Screenshots
See `ss/README.md`. Capture screenshots from your own successful terminal/Jenkins/Kubernetes runs; this bundle does not contain fake screenshots of tools that were not run.
