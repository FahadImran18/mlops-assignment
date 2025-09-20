"""
Configuration file for MLOps CI/CD Pipeline
This file contains group-specific settings including unique dataset configuration
"""

import os

# Group Configuration
GROUP_ID = os.environ.get('Fahad1', 'group_1')
GROUP_MEMBERS = ['Fahad', 'Member2']
ADMIN_MEMBER = 'Fahad'

# Dataset Configuration
DATASET_CONFIG = {
    'group_1': {
        'random_seed': 42,
        'n_samples': 1000,
        'n_features': 4,
        'noise_level': 0.1
    },
    'group_2': {
        'random_seed': 123,
        'n_samples': 1200,
        'n_features': 5,
        'noise_level': 0.15
    },
    'group_3': {
        'random_seed': 456,
        'n_samples': 800,
        'n_features': 6,
        'noise_level': 0.2
    },
    'group_4': {
        'random_seed': 789,
        'n_samples': 1500,
        'n_features': 4,
        'noise_level': 0.05
    }
}

# Application Configuration
APP_CONFIG = {
    'host': '0.0.0.0',
    'port': int(os.environ.get('PORT', 5000)),
    'debug': os.environ.get('FLASK_ENV') == 'development',
    'model_path': 'models/model.pkl',
    'data_path': 'data/dataset.csv'
}

# Model Configuration
MODEL_CONFIG = {
    'algorithm': 'RandomForestClassifier',
    'n_estimators': 100,
    'random_state': 42,
    'max_depth': 10,
    'min_samples_split': 2,
    'min_samples_leaf': 1
}

# CI/CD Configuration
CICD_CONFIG = {
    'docker_image': f'mlops-app-{GROUP_ID}',
    'docker_tag': 'latest',
    'test_coverage_threshold': 80,
    'max_line_length': 88
}

def get_dataset_config():
    """Get dataset configuration for the current group."""
    return DATASET_CONFIG.get(GROUP_ID, DATASET_CONFIG['group_1'])

def get_app_config():
    """Get application configuration."""
    return APP_CONFIG

def get_model_config():
    """Get model configuration."""
    return MODEL_CONFIG

def get_cicd_config():
    """Get CI/CD configuration."""
    return CICD_CONFIG
