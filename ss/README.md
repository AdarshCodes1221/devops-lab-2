# Screenshot checklist

Save real screenshots here after running each step successfully. Do not use screenshots of sample output as proof of execution.

Suggested filenames:
1. `01-git-release.png` — `git log --oneline --decorate --all` and `git tag --list` showing `v5.0.0-final`.
2. `02-docker.png` — `docker ps --filter name=video-encoder` plus `curl.exe -i http://localhost:8087` showing the ready message.
3. `03-kubernetes.png` — `kubectl get deployments,pods,services -l app=nginx -o wide`, showing 2 replicas and NodePort `30097`.
4. `04-terraform.png` — successful `terraform apply` / `terraform output -raw transcoder_output_file` and contents of `terraform/output.end`.
5. `05-ansible.png` — successful Ansible `stat` and `command` results for `terraform/output.end`.
6. `06-jenkins.png` — Jenkins job console showing Source Fetch, Media Linting, and Build Transcoder stages passing.

On Windows, use `Win + Shift + S`, save each capture to this `ss` folder, then re-zip the project if needed.
