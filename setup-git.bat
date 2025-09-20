@echo off
REM MLOps CI/CD Pipeline - Git Repository Setup Script for Windows
REM This script sets up the Git repository with proper branch structure

echo Setting up MLOps CI/CD Pipeline Git Repository...

REM Initialize Git repository if not already initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

REM Create initial commit (skip if already done)
echo Checking if initial commit exists...
git log --oneline -1 >nul 2>&1
if %errorlevel% neq 0 (
    echo Creating initial commit...
    git add .
    git commit -m "Initial commit: MLOps CI/CD Pipeline setup"
) else (
    echo Initial commit already exists, skipping...
)

REM Create and switch to dev branch
echo Creating dev branch...
git checkout -b dev
git push -u origin dev

REM Create and switch to test branch
echo Creating test branch...
git checkout -b test
git push -u origin test

REM Switch back to master branch
echo Switching back to master branch...
git checkout master
git push -u origin master

echo Git repository setup completed!
echo.
echo Branch structure:
echo - master: Production branch (triggers deployment)
echo - test: Testing branch (runs unit tests)
echo - dev: Development branch (code quality checks)
echo.
echo Next steps:
echo 1. Set up branch protection rules in GitHub
echo 2. Configure GitHub Secrets
echo 3. Set up Jenkins pipeline
echo 4. Start development on the dev branch
