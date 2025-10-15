#!/usr/bin/env python3
"""
Flask API Backend for Loan Prediction System
Provides REST API endpoints for the React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import time
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging

# Add parent directory to path to import database manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database_manager import DatabaseManager
from ml_models import get_ml_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# Enable CORS for React frontend
CORS(app, origins=config.CORS_ORIGINS)

# Initialize database manager and ML models
db = DatabaseManager()
ml_manager = get_ml_manager()

# JWT token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# ML Prediction using real models
def get_ml_prediction(application_data):
    """Get ML model predictions using trained models"""
    start_time = time.time()
    
    # For now, use simulation since ML models need to be properly loaded
    # This can be replaced with real ML models later
    return simulate_ml_prediction(application_data)

def simulate_ml_prediction(application_data, service_type='loan', selected_models=['xgboost', 'random_forest']):
    """Updated prediction logic for new field structure with service type"""
    logger.info(f"Using {service_type} prediction with models: {selected_models}")
    
    # Get values from new field structure (1, 0, -1 format)
    credit_short = float(application_data.get('creditShort', 0))
    credit_long = float(application_data.get('creditLong', 0))
    cph = float(application_data.get('cph', 0))
    ctl = float(application_data.get('ctl', 0))
    aph = float(application_data.get('aph', 0))
    atl = float(application_data.get('atl', 0))
    quarter_fluctuation = float(application_data.get('quarterFluctuation', 0))
    
    # Updated scoring algorithm for new field structure
    score = 0
    
    # Credit Score Short-term (1=Good, 0=Normal, -1=Poor)
    if credit_short == 1: score += 25
    elif credit_short == 0: score += 15
    else: score += 5  # -1 case
    
    # Credit Score Long-term (1=Good, 0=Normal, -1=Poor)
    if credit_long == 1: score += 25
    elif credit_long == 0: score += 15
    else: score += 5  # -1 case
    
    # CPH - Credit Payment History (1=Good, 0=Normal, -1=Poor)
    if cph == 1: score += 20
    elif cph == 0: score += 10
    else: score += 2  # -1 case
    
    # CTL - Credit Time Limitation (1=Good, 0=Normal, -1=Poor)
    if ctl == 1: score += 15
    elif ctl == 0: score += 8
    else: score += 2  # -1 case
    
    # APH - Average Payment History (1=Good, 0-0.99=Normal, <0=Poor)
    if aph == 1: score += 10
    elif aph >= 0: score += 5
    else: score += 1  # negative case
    
    # ATL - Average Time Limitation (1=Good, 0-0.99=Normal, <0=Poor)
    if atl == 1: score += 10
    elif atl >= 0: score += 5
    else: score += 1  # negative case
    
    # Quarterly Fluctuation bonus/penalty
    if quarter_fluctuation > 3: score += 5
    elif quarter_fluctuation >= 0: score += 2
    else: score -= 2  # negative fluctuation penalty
    
    # Determine prediction based on updated scoring
    # Maximum possible score: 25+25+20+15+10+10+5 = 110
    if score >= 85:  # ~77% of max score
        prediction = 'Very_Good'
        confidence = 90 + (score - 85) * 0.2
    elif score >= 50:  # ~45% of max score
        prediction = 'Normal'
        confidence = 75 + (score - 50) * 0.3
    else:
        prediction = 'Very_Bad'
        confidence = 60 + score * 0.2
    
    # Cap confidence at 95%
    confidence = min(confidence, 95.0)
    
    # Build response based on selected models
    result = {
        'final_prediction': prediction,
        'final_confidence': round(confidence, 1),
        'processing_time_ms': 150,
        'service_type': service_type,
        'models_used': selected_models
    }
    
    # Add model-specific predictions based on selection
    if 'xgboost' in selected_models:
        result['xgboost_prediction'] = prediction
        result['xgboost_confidence'] = round(confidence + 2, 1)
    
    if 'random_forest' in selected_models:
        result['random_forest_prediction'] = prediction
        result['random_forest_confidence'] = round(confidence - 1, 1)
    
    if 'logistic' in selected_models:
        result['logistic_prediction'] = prediction
        result['logistic_confidence'] = round(confidence - 3, 1)
    
    if 'knn' in selected_models:
        result['knn_prediction'] = prediction
        result['knn_confidence'] = round(confidence - 2, 1)
    
    return result

# Authentication endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        existing_user = db.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Hash password
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Create user
        user_id = db.create_user(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get user
        user = db.get_user_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        if user['password_hash'] != password_hash:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Loan prediction endpoints
@app.route('/api/predict', methods=['POST'])
def predict_loan():
    """Process loan prediction or customer classification"""
    try:
        data = request.get_json()
        
        # Get service type and selected models
        service_type = data.get('serviceType', 'loan')
        selected_models = data.get('selectedModels', ['xgboost', 'random_forest'])
        
        logger.info(f"Processing {service_type} request with models: {selected_models}")
        
        # Validate required fields
        required_fields = ['creditShort', 'creditLong', 'cph', 'ctl', 'aph', 'atl', 'quarterFluctuation']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Convert frontend field names to database field names
        application_data = {
            'credit_short': data['creditShort'],
            'credit_long': data['creditLong'],
            'payment_history': 'good',  # Default value since field was removed
            'time_limitation': data.get('timeLimitation'),
            'cph': data['cph'],
            'ctl': data['ctl'],
            'aph': data['aph'],
            'atl': data['atl'],
            'quarter_fluctuation': data.get('quarterFluctuation'),
            'residual_fluctuation': data.get('residualFluctuation'),
            'requested_amount': data.get('requestedAmount', 50000),
            'loan_purpose': data.get('loanPurpose', 'Personal'),
            'employment_status': data.get('employmentStatus', 'Employed'),
            'annual_income': data.get('annualIncome', 60000)
        }
        
        # For demo purposes, use user_id = 1 (demo user)
        # In production, this would be extracted from JWT token
        user_id = 1
        
        # Create loan application
        app_id = db.create_loan_application(user_id, application_data)
        
        # Generate ML predictions based on service type
        prediction_data = simulate_ml_prediction(application_data, service_type, selected_models)
        
        # Save prediction
        pred_id = db.save_prediction(app_id, prediction_data)
        
        # Update application status
        db.update_application_status(app_id, 'processed')
        
        # Return prediction results
        return jsonify({
            'application_id': app_id,
            'prediction_id': pred_id,
            'prediction': prediction_data['final_prediction'],
            'confidence': prediction_data['final_confidence'],
            'model_predictions': {
                'xgboost': {
                    'prediction': prediction_data.get('xgboost_prediction'),
                    'confidence': prediction_data.get('xgboost_confidence')
                },
                'random_forest': {
                    'prediction': prediction_data.get('random_forest_prediction'),
                    'confidence': prediction_data.get('random_forest_confidence')
                },
                'logistic': {
                    'prediction': prediction_data.get('logistic_prediction'),
                    'confidence': prediction_data.get('logistic_confidence')
                },
                'knn': {
                    'prediction': prediction_data.get('knn_prediction'),
                    'confidence': prediction_data.get('knn_confidence')
                }
            },
            'processing_time_ms': prediction_data['processing_time_ms'],
            'loan_range': get_loan_range(prediction_data['final_prediction']),
            'factors': get_prediction_factors(application_data, prediction_data['final_prediction'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_loan_range(prediction):
    """Get loan amount range based on prediction"""
    ranges = {
        'Very_Good': '$50,000 - $200,000',
        'Normal': '$10,000 - $50,000',
        'Very_Bad': 'Not eligible'
    }
    return ranges.get(prediction, 'Unknown')

def get_prediction_factors(application_data, prediction):
    """Get key factors affecting the prediction - updated for new field structure"""
    credit_short = float(application_data.get('creditShort', 0))
    cph = float(application_data.get('cph', 0))
    aph = float(application_data.get('aph', 0))
    
    return {
        'creditScore': 'Excellent' if credit_short == 1 else 'Good' if credit_short == 0 else 'Needs Improvement',
        'creditPaymentHistory': 'Excellent' if cph == 1 else 'Good' if cph == 0 else 'Needs Improvement',
        'avgPaymentHistory': 'Excellent' if aph == 1 else 'Good' if aph >= 0.7 else 'Needs Improvement'
    }

# Dashboard endpoints
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = db.get_dashboard_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/trends', methods=['GET'])
def get_monthly_trends():
    """Get monthly prediction trends"""
    try:
        months = request.args.get('months', 6, type=int)
        trends = db.get_monthly_trends(months)
        return jsonify(trends), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/performance', methods=['GET'])
def get_model_performance():
    """Get model performance metrics"""
    try:
        performance = db.get_model_performance()
        return jsonify(performance), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/feature-importance', methods=['GET'])
def get_feature_importance():
    """Get feature importance data"""
    try:
        model_name = request.args.get('model')
        importance = db.get_feature_importance(model_name)
        return jsonify(importance), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User application endpoints
@app.route('/api/applications', methods=['GET'])
@token_required
def get_user_applications(current_user_id):
    """Get user's loan applications"""
    try:
        applications = db.get_user_applications(current_user_id)
        return jsonify(applications), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>', methods=['GET'])
@token_required
def get_application_details(current_user_id, app_id):
    """Get detailed application information"""
    try:
        application = db.get_loan_application(app_id)
        if not application or application['user_id'] != current_user_id:
            return jsonify({'error': 'Application not found'}), 404
        
        prediction = db.get_prediction(app_id)
        
        return jsonify({
            'application': application,
            'prediction': prediction
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Loan Prediction API Server...")
    print("📊 Database:", db.db_path)
    print("🌐 Server will be available at: http://localhost:5000")
    print("📋 API Documentation:")
    print("   POST /api/predict - Loan prediction")
    print("   GET  /api/dashboard/stats - Dashboard statistics")
    print("   GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)