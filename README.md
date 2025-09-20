# MLOps CI/CD Pipeline Assignment

This project implements a complete CI/CD pipeline for a machine learning application using Flask, Docker, GitHub Actions, and Jenkins.

## Project Structure

```
├── app.py                 # Flask application with ML model
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── Jenkinsfile           # Jenkins pipeline configuration
├── tests/                # Unit tests
│   ├── __init__.py
│   └── test_app.py
├── .github/workflows/    # GitHub Actions workflows
│   ├── code-quality.yml  # Code quality checks (flake8)
│   ├── unit-tests.yml    # Unit testing workflow
│   └── deploy.yml        # Deployment workflow
├── .flake8              # Flake8 configuration
├── pytest.ini          # Pytest configuration
├── .gitignore          # Git ignore rules
└── .dockerignore       # Docker ignore rules
```

## Features

- **Machine Learning Model**: Random Forest classifier with synthetic dataset
- **Flask API**: RESTful endpoints for predictions and model management
- **Docker Containerization**: Complete containerization with health checks
- **CI/CD Pipeline**: Multi-stage pipeline with quality gates
- **Code Quality**: Automated code quality checks using flake8
- **Unit Testing**: Comprehensive test suite with coverage reporting
- **Notifications**: Email notifications for successful deployments

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /predict` - Make predictions using the ML model
- `GET /model/info` - Get model information
- `POST /retrain` - Retrain the model

## CI/CD Pipeline Flow

### 1. Development Branch (dev)
- Developers push changes to the `dev` branch
- Admin approval required for merging (Pull Request workflow)
- GitHub Actions triggers code quality checks using flake8
- Only code that passes quality checks can be merged

### 2. Test Branch (test)
- Completed features are merged from `dev` to `test` via Pull Request
- GitHub Actions triggers unit testing workflow
- Automated test cases are executed with coverage reporting
- Only passing tests can be merged to master

### 3. Master Branch (master)
- Successful test results allow merging to `master`
- GitHub Actions triggers deployment workflow
- Jenkins job is triggered for containerization
- Docker image is built and pushed to Docker Hub
- Email notification is sent to administrator

## Setup Instructions

### Prerequisites

1. **Git**: For version control
2. **Python 3.9+**: For running the application
3. **Docker**: For containerization
4. **GitHub Account**: For repository and GitHub Actions
5. **Jenkins**: For deployment pipeline
6. **Docker Hub Account**: For storing Docker images

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mlops-assignment
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

6. **Run code quality checks**:
   ```bash
   flake8 .
   ```

### Docker Setup

1. **Build Docker image**:
   ```bash
   docker build -t mlops-app .
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Test the application**:
   ```bash
   curl http://localhost:5000/health
   ```

### GitHub Setup

1. **Create GitHub repository** and push code
2. **Set up branch protection rules**:
   - Require pull request reviews for `dev` and `test` branches
   - Require status checks to pass before merging
   - Restrict pushes to `master` branch

3. **Configure GitHub Secrets**:
   - `DOCKER_USERNAME`: Docker Hub username
   - `DOCKER_PASSWORD`: Docker Hub password
   - `JENKINS_TOKEN`: Jenkins API token
   - `JENKINS_URL`: Jenkins server URL
   - `ADMIN_EMAIL`: Administrator email address
   - `EMAIL_USERNAME`: Email username for notifications
   - `EMAIL_PASSWORD`: Email password for notifications

### Jenkins Setup

1. **Install required plugins**:
   - Docker Pipeline
   - Email Extension
   - GitHub Integration

2. **Create new pipeline job**:
   - Name: `mlops-deploy`
   - Type: Pipeline
   - Pipeline script from SCM: Git
   - Repository URL: Your GitHub repository
   - Script Path: `Jenkinsfile`

3. **Configure credentials**:
   - `docker-hub-username`: Docker Hub username
   - `docker-hub-password`: Docker Hub password
   - `admin-email`: Administrator email
   - `email-username`: Email username
   - `email-password`: Email password

## Workflow Examples

### Making a Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.5, -0.3, 0.8, -0.1]}'
```

### Retraining the Model

```bash
curl -X POST http://localhost:5000/retrain
```

### Health Check

```bash
curl http://localhost:5000/health
```

## Group Assignment Requirements

### Team Structure
- **2 members per group**
- **1 admin per group** (responsible for approving pull requests)
- **Unique dataset per group** (implemented with different random seeds)

### Branch Strategy
- `dev`: Development branch (requires admin approval)
- `test`: Testing branch (requires passing unit tests)
- `master`: Production branch (triggers deployment)

### Quality Gates
1. **Code Quality**: flake8 checks on `dev` branch
2. **Unit Testing**: Automated tests on `test` branch
3. **Deployment**: Jenkins pipeline on `master` branch

## Monitoring and Notifications

- **Email notifications** sent to administrator on successful deployment
- **Health checks** implemented for Docker containers
- **Coverage reporting** for unit tests
- **Build status** visible in GitHub Actions

## Troubleshooting

### Common Issues

1. **Docker build fails**: Check Dockerfile syntax and dependencies
2. **Tests fail**: Ensure all dependencies are installed
3. **Jenkins job fails**: Check credentials and network connectivity
4. **Email notifications not working**: Verify email credentials and SMTP settings

### Logs and Debugging

- **Application logs**: Check Docker container logs
- **GitHub Actions logs**: Available in the Actions tab
- **Jenkins logs**: Available in the Jenkins console output

## Contributing

1. Create feature branch from `dev`
2. Make changes and test locally
3. Push to `dev` branch
4. Create pull request for admin review
5. After approval, merge to `test` for testing
6. After successful tests, merge to `master` for deployment

## License

This project is created for educational purposes as part of the MLOps assignment.
