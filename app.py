"""
Flask application for MLOps CI/CD Pipeline Assignment
This application serves a machine learning model for predictions.
"""

import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import logging
from config import get_dataset_config, get_app_config, get_model_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for model and data
model = None
app_config = get_app_config()
model_path = app_config['model_path']
data_path = app_config['data_path']

def load_or_create_model():
    """Load existing model or create a new one if it doesn't exist."""
    global model
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            logger.info("Model loaded successfully from %s", model_path)
        except Exception as e:
            logger.error("Error loading model: %s", str(e))
            model = None
    else:
        logger.info("No existing model found. Creating new model...")
        create_and_train_model()

def create_and_train_model():
    """Create and train a new model with sample data."""
    global model
    
    try:
        # Get group-specific dataset configuration
        dataset_config = get_dataset_config()
        model_config = get_model_config()
        
        # Create sample dataset (unique for each group)
        np.random.seed(dataset_config['random_seed'])
        n_samples = dataset_config['n_samples']
        n_features = dataset_config['n_features']
        
        # Generate synthetic data
        X = np.random.randn(n_samples, n_features)
        # Create target variable based on features
        y = (np.sum(X, axis=1) > 0).astype(int)
        
        # Add noise to make it more realistic
        noise = np.random.normal(0, dataset_config['noise_level'], n_samples)
        y = (np.sum(X, axis=1) + noise > 0).astype(int)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=dataset_config['random_seed']
        )
        
        # Train the model
        model = RandomForestClassifier(
            n_estimators=model_config['n_estimators'],
            random_state=model_config['random_state'],
            max_depth=model_config['max_depth'],
            min_samples_split=model_config['min_samples_split'],
            min_samples_leaf=model_config['min_samples_leaf']
        )
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info("Model trained successfully. Accuracy: %.4f", accuracy)
        
        # Save the model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)
        
        # Save the dataset
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(n_features)])
        df['target'] = y
        df.to_csv(data_path, index=False)
        
        logger.info("Model and dataset saved successfully")
        
    except Exception as e:
        logger.error("Error creating model: %s", str(e))
        model = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'MLOps CI/CD Pipeline Application is running'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint."""
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get input data
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(max(probability)),
            'features': data['features']
        })
        
    except Exception as e:
        logger.error("Prediction error: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': type(model).__name__,
        'n_features': model.n_features_in_ if hasattr(model, 'n_features_in_') else 'Unknown',
        'n_estimators': model.n_estimators if hasattr(model, 'n_estimators') else 'Unknown'
    })

@app.route('/retrain', methods=['POST'])
def retrain_model():
    """Retrain the model endpoint."""
    try:
        create_and_train_model()
        return jsonify({'message': 'Model retrained successfully'})
    except Exception as e:
        logger.error("Retraining error: %s", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load or create model on startup
    load_or_create_model()
    
    # Run the application
    app.run(
        host=app_config['host'],
        port=app_config['port'],
        debug=app_config['debug']
    )
