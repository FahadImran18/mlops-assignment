# MLOps CI/CD Pipeline - Complete Setup Guide

This guide provides step-by-step instructions for setting up the complete CI/CD pipeline for your MLOps assignment.

## Prerequisites

Before starting, ensure you have the following installed:

- **Git** (version 2.0+)
- **Python** (version 3.9+)
- **Docker** (version 20.0+)
- **Docker Compose** (version 2.0+)
- **GitHub Account**
- **Jenkins** (version 2.400+)
- **Docker Hub Account**

## Step 1: Project Setup

### 1.1 Clone and Initialize Repository

```bash
# Clone your repository (replace with your actual repository URL)
git clone https://github.com/FahadImran18/mlops-assignment.git
cd mlops-assignment

# Run the setup script
# On Windows:
setup-git.bat
# On Linux/Mac:
chmod +x setup-git.sh
./setup-git.sh
```

### 1.2 Configure Group Settings

Edit `config.py` to set your group-specific configuration:

```python
# Update these values for your group
GROUP_ID = 'group_1'  # Change to your group number
GROUP_MEMBERS = ['YourName', 'PartnerName']  # Update with actual names
ADMIN_MEMBER = 'YourName'  # Set the admin member
```

## Step 2: GitHub Repository Setup

### 2.1 Create GitHub Repository

1. Go to GitHub and create a new repository
2. Name it `mlops-assignment` (or your preferred name)
3. Make it private (recommended for assignments)
4. Don't initialize with README (we already have one)

### 2.2 Push Code to GitHub

```bash
# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/your-username/mlops-assignment.git

# Push all branches
git push -u origin master
git push -u origin dev
git push -u origin test
```

### 2.3 Set Up Branch Protection Rules

1. Go to your repository settings
2. Navigate to "Branches"
3. Add rule for `dev` branch:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Select "code-quality" workflow
4. Add rule for `test` branch:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Select "unit-tests" workflow
5. Add rule for `master` branch:
   - Restrict pushes to this branch
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Select "deploy" workflow

### 2.4 Configure GitHub Secrets

Go to repository settings → Secrets and variables → Actions, and add:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password
- `JENKINS_TOKEN`: Jenkins API token (we'll create this later)
- `JENKINS_URL`: Your Jenkins server URL
- `ADMIN_EMAIL`: Administrator email address
- `EMAIL_USERNAME`: Email username for notifications
- `EMAIL_PASSWORD`: Email password for notifications

## Step 3: Jenkins Setup

### 3.1 Install Required Plugins

In Jenkins, go to Manage Jenkins → Manage Plugins and install:

- Docker Pipeline
- Email Extension
- GitHub Integration
- Build Timeout
- Timestamper

### 3.2 Create Jenkins API Token

1. Go to your user profile in Jenkins
2. Click "Configure"
3. In the "API Token" section, click "Add new Token"
4. Give it a name and click "Generate"
5. Copy the token and save it as `JENKINS_TOKEN` in GitHub Secrets

### 3.3 Create Pipeline Job

1. Click "New Item" in Jenkins
2. Enter name: `mlops-deploy`
3. Select "Pipeline"
4. Click "OK"
5. In the pipeline configuration:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your GitHub repository URL
   - Credentials: Add your GitHub credentials if needed
   - Script Path: `Jenkinsfile`
6. Save the configuration

### 3.4 Configure Jenkins Credentials

Go to Manage Jenkins → Manage Credentials and add:

- `docker-hub-username`: Your Docker Hub username
- `docker-hub-password`: Your Docker Hub password
- `admin-email`: Administrator email address
- `email-username`: Email username for notifications
- `email-password`: Email password for notifications

### 3.5 Configure Email Notifications

1. Go to Manage Jenkins → Configure System
2. Find "E-mail Notification" section
3. Configure SMTP settings:
   - SMTP server: smtp.gmail.com (for Gmail)
   - Default user e-mail suffix: your domain
   - Use SMTP Authentication: Yes
   - User Name: Your email username
   - Password: Your email password
   - Use SSL: Yes
   - SMTP Port: 587

## Step 4: Docker Hub Setup

### 4.1 Create Docker Hub Account

1. Go to https://hub.docker.com
2. Create an account if you don't have one
3. Create a new repository named `mlops-app`

### 4.2 Test Docker Build Locally

```bash
# Build the Docker image
docker build -t mlops-app .

# Test the container
docker run -p 5000:5000 mlops-app

# Test the health endpoint
curl http://localhost:5000/health
```

## Step 5: Testing the Pipeline

### 5.1 Test Code Quality Workflow

1. Make a small change to `app.py`
2. Push to `dev` branch
3. Check GitHub Actions tab to see if the workflow runs
4. Verify flake8 checks pass

### 5.2 Test Unit Testing Workflow

1. Create a pull request from `dev` to `test`
2. Check if the unit tests workflow runs
3. Verify all tests pass

### 5.3 Test Deployment Workflow

1. Create a pull request from `test` to `master`
2. Check if the deployment workflow runs
3. Verify Jenkins job is triggered
4. Check if Docker image is pushed to Docker Hub
5. Verify email notification is sent

## Step 6: Group Workflow

### 6.1 Development Process

1. **Feature Development**:
   - Create feature branch from `dev`
   - Make changes and test locally
   - Push to `dev` branch

2. **Code Review**:
   - Admin reviews the changes
   - Approves or requests modifications
   - Merges to `dev` after approval

3. **Testing**:
   - Create pull request from `dev` to `test`
   - Automated tests run
   - Merge to `test` after tests pass

4. **Deployment**:
   - Create pull request from `test` to `master`
   - Jenkins pipeline runs
   - Application is deployed

### 6.2 Admin Responsibilities

- Review and approve pull requests to `dev` branch
- Monitor CI/CD pipeline health
- Handle deployment issues
- Manage repository settings

## Step 7: Monitoring and Maintenance

### 7.1 Health Checks

- Monitor application health: `curl http://localhost:5000/health`
- Check Docker container status: `docker ps`
- Review Jenkins build logs
- Monitor GitHub Actions workflows

### 7.2 Troubleshooting

**Common Issues:**

1. **GitHub Actions fail**:
   - Check secrets configuration
   - Verify workflow syntax
   - Check repository permissions

2. **Jenkins job fails**:
   - Verify credentials
   - Check Jenkins plugins
   - Review build logs

3. **Docker build fails**:
   - Check Dockerfile syntax
   - Verify dependencies
   - Check Docker Hub credentials

4. **Email notifications not working**:
   - Verify SMTP settings
   - Check email credentials
   - Test email configuration

## Step 8: Assignment Submission

### 8.1 Documentation

Ensure you have:
- Complete README.md with setup instructions
- Working CI/CD pipeline
- All required workflows functioning
- Proper branch protection rules
- Email notifications working

### 8.2 Demo Preparation

Prepare to demonstrate:
- Code quality checks on `dev` branch
- Unit testing on `test` branch
- Deployment pipeline on `master` branch
- Admin approval workflow
- Email notifications
- Docker containerization

## Support and Resources

- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Docker Documentation**: https://docs.docker.com/
- **Flask Documentation**: https://flask.palletsprojects.com/

## Group Assignment Checklist

- [ ] Repository created with proper branch structure
- [ ] GitHub Actions workflows configured
- [ ] Jenkins pipeline set up
- [ ] Docker containerization working
- [ ] Branch protection rules configured
- [ ] Admin approval workflow functioning
- [ ] Code quality checks (flake8) working
- [ ] Unit tests passing
- [ ] Email notifications working
- [ ] Unique dataset per group implemented
- [ ] Documentation complete
- [ ] Demo ready

Good luck with your MLOps assignment!
