$ErrorActionPreference = 'Stop'

if (Test-Path '.git') {
    throw 'A .git directory already exists. Run this script only once in a clean project copy.'
}

git init -b main
if (-not (git config user.name)) { git config user.name 'DevOps Lab User' }
if (-not (git config user.email)) { git config user.email 'devops-lab@example.local' }
git add README.md
git commit -m 'Initialize OTT transcoder repository'

git switch -c media-encoder
git add .gitignore app.py Dockerfile Jenkinsfile k8s terraform ansible scripts
git commit -m 'Add media encoder app and delivery resources'

git switch -c release-v5.0
git add transcode.conf
git commit -m 'Set transcoder maximum bitrate to 4k for v5.0'

git switch main
git merge media-encoder --no-edit
git merge release-v5.0 --no-edit
git tag -a v5.0.0-final -m 'Final media encoder v5.0.0 release'

Write-Host "`n--- Branches ---"
git branch --all
Write-Host "`n--- Recent history ---"
git log --oneline --decorate --all -10
Write-Host "`n--- Tags ---"
git tag --list
