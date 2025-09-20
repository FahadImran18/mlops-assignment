"""
Unit tests for the Flask application
"""

import pytest
import json
import os
import tempfile
import shutil
from app import app, model, create_and_train_model

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    
    # Create temporary directories for test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Override paths for testing
        global model_path, data_path
        model_path = os.path.join(temp_dir, 'test_model.pkl')
        data_path = os.path.join(temp_dir, 'test_dataset.csv')
        
        with app.test_client() as client:
            yield client

@pytest.fixture
def sample_features():
    """Sample features for testing."""
    return [0.5, -0.3, 0.8, -0.1]

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'MLOps CI/CD Pipeline Application is running' in data['message']

def test_model_info_without_model(client):
    """Test model info endpoint when no model is loaded."""
    response = client.get('/model/info')
    assert response.status_code == 500
    
    data = json.loads(response.data)
    assert 'error' in data

def test_predict_without_model(client):
    """Test prediction endpoint when no model is loaded."""
    response = client.post('/predict', 
                          json={'features': [0.5, -0.3, 0.8, -0.1]})
    assert response.status_code == 500
    
    data = json.loads(response.data)
    assert 'error' in data

def test_predict_invalid_input(client):
    """Test prediction endpoint with invalid input."""
    # Test with no features
    response = client.post('/predict', json={})
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    
    # Test with invalid JSON
    response = client.post('/predict', data='invalid json')
    assert response.status_code == 400

def test_retrain_model(client):
    """Test model retraining endpoint."""
    response = client.post('/retrain')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'retrained successfully' in data['message']

def test_model_creation():
    """Test model creation and training function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        global model_path, data_path
        model_path = os.path.join(temp_dir, 'test_model.pkl')
        data_path = os.path.join(temp_dir, 'test_dataset.csv')
        
        # Test model creation
        create_and_train_model()
        
        # Check if model file was created
        assert os.path.exists(model_path)
        assert os.path.exists(data_path)
        
        # Check if model can be loaded
        import joblib
        loaded_model = joblib.load(model_path)
        assert loaded_model is not None

def test_predict_with_valid_model(client):
    """Test prediction with a valid model."""
    # First retrain to ensure we have a model
    client.post('/retrain')
    
    # Test prediction
    response = client.post('/predict', 
                          json={'features': [0.5, -0.3, 0.8, -0.1]})
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'prediction' in data
    assert 'probability' in data
    assert 'features' in data
    assert isinstance(data['prediction'], int)
    assert isinstance(data['probability'], float)

def test_model_info_with_model(client):
    """Test model info endpoint with a loaded model."""
    # First retrain to ensure we have a model
    client.post('/retrain')
    
    response = client.get('/model/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'model_type' in data
    assert 'n_features' in data
    assert 'n_estimators' in data

if __name__ == '__main__':
    pytest.main([__file__])
