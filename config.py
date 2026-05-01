#!/usr/bin/env python3
"""
Configuration file for Rural Financial Inclusion System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Secret key for JWT tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024'
    
    # Debug mode
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database/loan_prediction.db')
    
    # JWT settings
    JWT_EXPIRATION_DELTA = timedelta(days=7)
    
    # ML Models
    MODELS_DIR = os.environ.get('MODELS_DIR', 'models')
    
    # Application settings
    APP_NAME = "PALP AI - Pre-Approved Loan Prediction"
    APP_VERSION = "1.0.0"
    
    # Loan ranges based on classification
    LOAN_RANGES = {
        'Very_Good': {
            'min': 50000,
            'max': 200000,
            'interest_rate': '8-10%',
            'description': 'Excellent credit profile'
        },
        'Normal': {
            'min': 10000,
            'max': 50000,
            'interest_rate': '10-14%',
            'description': 'Good credit profile'
        },
        'Very_Bad': {
            'min': 5000,
            'max': 10000,
            'interest_rate': '14-18%',
            'description': 'Needs improvement'
        }
    }
    
    # Government schemes
    GOVERNMENT_SCHEMES = {
        'Very_Good': [
            {
                'name': 'PM-KISAN Credit Card',
                'description': 'For farmers with excellent credit',
                'max_amount': 300000,
                'interest_rate': '7%'
            },
            {
                'name': 'Mudra Loan (Tarun)',
                'description': 'For business expansion',
                'max_amount': 1000000,
                'interest_rate': '8-10%'
            },
            {
                'name': 'Stand-Up India',
                'description': 'For SC/ST/Women entrepreneurs',
                'max_amount': 10000000,
                'interest_rate': '9%'
            }
        ],
        'Normal': [
            {
                'name': 'Mudra Loan (Kishor)',
                'description': 'For small business growth',
                'max_amount': 500000,
                'interest_rate': '10-12%'
            },
            {
                'name': 'PM SVANidhi',
                'description': 'For street vendors',
                'max_amount': 50000,
                'interest_rate': '12%'
            },
            {
                'name': 'SHG Bank Linkage',
                'description': 'Self-Help Group loans',
                'max_amount': 100000,
                'interest_rate': '11%'
            }
        ],
        'Very_Bad': [
            {
                'name': 'Mudra Loan (Shishu)',
                'description': 'Micro-loans for beginners',
                'max_amount': 50000,
                'interest_rate': '14%'
            },
            {
                'name': 'SHG Micro-credit',
                'description': 'Small loans through SHGs',
                'max_amount': 25000,
                'interest_rate': '15%'
            },
            {
                'name': 'NRLM Support',
                'description': 'National Rural Livelihood Mission',
                'max_amount': 30000,
                'interest_rate': '14%'
            }
        ]
    }

# Create config instance
config = Config()
