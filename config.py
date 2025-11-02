#!/usr/bin/env python3
"""
Configuration Management for Loan Prediction System
Handles environment variables and system configuration
"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/loan_prediction.db')
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', 'localhost')
    API_PORT = int(os.getenv('API_PORT', 5000))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # ML Model Configuration
    MODEL_VERSION = os.getenv('MODEL_VERSION', '1.0')
    MODELS_DIR = os.getenv('MODELS_DIR', '../')
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.75))
    
    # Business Rules
    MIN_CREDIT_SCORE = int(os.getenv('MIN_CREDIT_SCORE', 300))
    MAX_CREDIT_SCORE = int(os.getenv('MAX_CREDIT_SCORE', 850))
    MAX_LOAN_AMOUNT = int(os.getenv('MAX_LOAN_AMOUNT', 500000))
    
    # Security Configuration
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 168))  # 7 days
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 6))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Performance Configuration
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 100))
    REQUEST_TIMEOUT_SECONDS = int(os.getenv('REQUEST_TIMEOUT_SECONDS', 30))
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'path': cls.DATABASE_PATH,
            'url': cls.DATABASE_URL,
            'backup_enabled': True,
            'backup_interval_hours': 24
        }
    
    @classmethod
    def get_ml_config(cls) -> Dict[str, Any]:
        """Get ML model configuration"""
        return {
            'models_dir': cls.MODELS_DIR,
            'version': cls.MODEL_VERSION,
            'confidence_threshold': cls.CONFIDENCE_THRESHOLD,
            'feature_count': 10,
            'supported_models': ['xgboost', 'random_forest', 'logistic', 'knn', 'mlp']
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration"""
        return {
            'host': cls.API_HOST,
            'port': cls.API_PORT,
            'debug': cls.DEBUG,
            'cors_origins': cls.CORS_ORIGINS,
            'max_requests_per_minute': cls.MAX_REQUESTS_PER_MINUTE,
            'timeout_seconds': cls.REQUEST_TIMEOUT_SECONDS
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        errors = []
        
        # Check database path
        db_dir = Path(cls.DATABASE_PATH).parent
        if not db_dir.exists():
            try:
                db_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create database directory: {e}")
        
        # Check models directory
        if not Path(cls.MODELS_DIR).exists():
            errors.append(f"Models directory not found: {cls.MODELS_DIR}")
        
        # Check numeric ranges
        if not (300 <= cls.MIN_CREDIT_SCORE <= cls.MAX_CREDIT_SCORE <= 850):
            errors.append("Invalid credit score range")
        
        if cls.CONFIDENCE_THRESHOLD < 0 or cls.CONFIDENCE_THRESHOLD > 1:
            errors.append("Confidence threshold must be between 0 and 1")
        
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   • {error}")
            return False
        
        return True
    
    @classmethod
    def create_env_file(cls, filepath: str = '.env') -> bool:
        """Create environment file with default values"""
        env_content = f"""# Loan Prediction System Configuration
# Generated automatically - modify as needed

# Database Configuration
DATABASE_PATH={cls.DATABASE_PATH}

# Flask Configuration
SECRET_KEY={cls.SECRET_KEY}
FLASK_ENV={cls.FLASK_ENV}
FLASK_DEBUG={cls.DEBUG}

# API Configuration
API_HOST={cls.API_HOST}
API_PORT={cls.API_PORT}
CORS_ORIGINS={','.join(cls.CORS_ORIGINS)}

# ML Model Configuration
MODEL_VERSION={cls.MODEL_VERSION}
MODELS_DIR={cls.MODELS_DIR}
CONFIDENCE_THRESHOLD={cls.CONFIDENCE_THRESHOLD}

# Business Rules
MIN_CREDIT_SCORE={cls.MIN_CREDIT_SCORE}
MAX_CREDIT_SCORE={cls.MAX_CREDIT_SCORE}
MAX_LOAN_AMOUNT={cls.MAX_LOAN_AMOUNT}

# Security Configuration
JWT_EXPIRATION_HOURS={cls.JWT_EXPIRATION_HOURS}
PASSWORD_MIN_LENGTH={cls.PASSWORD_MIN_LENGTH}

# Logging Configuration
LOG_LEVEL={cls.LOG_LEVEL}
LOG_FILE={cls.LOG_FILE}

# Performance Configuration
MAX_REQUESTS_PER_MINUTE={cls.MAX_REQUESTS_PER_MINUTE}
REQUEST_TIMEOUT_SECONDS={cls.REQUEST_TIMEOUT_SECONDS}

# Frontend Configuration (for React)
REACT_APP_API_URL=http://{cls.API_HOST}:{cls.API_PORT}/api
REACT_APP_APP_NAME=LoanPredict AI
REACT_APP_VERSION={cls.MODEL_VERSION}
"""
        
        try:
            with open(filepath, 'w') as f:
                f.write(env_content)
            print(f"✅ Environment file created: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to create environment file: {e}")
            return False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    
    # Enhanced security for production
    JWT_EXPIRATION_HOURS = 24  # Shorter token expiration
    MAX_REQUESTS_PER_MINUTE = 60  # Lower rate limit
    
    @classmethod
    def validate_production_config(cls) -> bool:
        """Additional validation for production"""
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            print("❌ SECRET_KEY must be set for production")
            return False
        
        if cls.DEBUG:
            print("❌ DEBUG must be False in production")
            return False
        
        return cls.validate_config()

class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    DATABASE_PATH = 'test_database.db'
    SECRET_KEY = 'test-secret-key'

# Configuration factory
def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestConfig
    }
    
    return config_map.get(env, DevelopmentConfig)

# Load environment variables from .env file if it exists
def load_env_file(filepath: str = '.env'):
    """Load environment variables from file"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

# Initialize configuration
load_env_file()
config = get_config()

if __name__ == "__main__":
    print("🔧 Loan Prediction System Configuration")
    print("=" * 40)
    
    # Validate configuration
    if config.validate_config():
        print("✅ Configuration is valid")
        
        # Print current configuration
        print(f"\n📊 Current Settings:")
        print(f"   Environment: {config.FLASK_ENV}")
        print(f"   Debug: {config.DEBUG}")
        print(f"   Database: {config.DATABASE_PATH}")
        print(f"   API: {config.API_HOST}:{config.API_PORT}")
        print(f"   Models: {config.MODELS_DIR}")
        print(f"   Confidence Threshold: {config.CONFIDENCE_THRESHOLD}")
        
        # Offer to create .env file
        if not os.path.exists('.env'):
            response = input("\n❓ Create .env file with current settings? (y/n): ")
            if response.lower() == 'y':
                config.create_env_file()
    else:
        print("❌ Configuration validation failed")
        exit(1)