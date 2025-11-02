-- Loan Prediction Database Schema
-- This schema supports the ML models and web application

-- Create database (PostgreSQL)
-- CREATE DATABASE loan_prediction_db;

-- Users table for authentication and user management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Loan applications table - stores user loan application data
CREATE TABLE loan_applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Financial features used by ML models
    credit_short DECIMAL(10,2) NOT NULL,
    credit_long DECIMAL(10,2) NOT NULL,
    payment_history VARCHAR(20) NOT NULL CHECK (payment_history IN ('excellent', 'good', 'fair', 'poor')),
    time_limitation DECIMAL(5,2),
    cph DECIMAL(5,4) NOT NULL, -- Credit Payment History
    ctl DECIMAL(5,4) NOT NULL, -- Credit Time Limitation  
    aph DECIMAL(5,4) NOT NULL, -- Average Payment History
    atl DECIMAL(5,4) NOT NULL, -- Average Time Limitation
    quarter_fluctuation INTEGER,
    residual_fluctuation INTEGER,
    
    -- Application metadata
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processed', 'approved', 'rejected')),
    
    -- Additional loan details
    requested_amount DECIMAL(12,2),
    loan_purpose VARCHAR(100),
    employment_status VARCHAR(50),
    annual_income DECIMAL(12,2),
    
    CONSTRAINT valid_credit_scores CHECK (credit_short >= 0 AND credit_long >= 0),
    CONSTRAINT valid_ratios CHECK (cph BETWEEN 0 AND 1 AND ctl BETWEEN 0 AND 1 AND aph BETWEEN 0 AND 1 AND atl BETWEEN 0 AND 1)
);

-- Predictions table - stores ML model predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES loan_applications(id) ON DELETE CASCADE,
    
    -- Model predictions
    xgboost_prediction VARCHAR(20),
    xgboost_confidence DECIMAL(5,2),
    random_forest_prediction VARCHAR(20),
    random_forest_confidence DECIMAL(5,2),
    logistic_prediction VARCHAR(20),
    logistic_confidence DECIMAL(5,2),
    knn_prediction VARCHAR(20),
    knn_confidence DECIMAL(5,2),
    
    -- Final ensemble prediction
    final_prediction VARCHAR(20) NOT NULL CHECK (final_prediction IN ('Very_Good', 'Normal', 'Very_Bad')),
    final_confidence DECIMAL(5,2) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Model metadata
    model_version VARCHAR(20) DEFAULT '1.0',
    processing_time_ms INTEGER,
    
    CONSTRAINT valid_predictions CHECK (
        xgboost_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR xgboost_prediction IS NULL
        AND random_forest_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR random_forest_prediction IS NULL
        AND logistic_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR logistic_prediction IS NULL
        AND knn_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR knn_prediction IS NULL
    )
);

-- Model performance tracking
CREATE TABLE model_performance (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    accuracy DECIMAL(5,2),
    precision_score DECIMAL(5,2),
    recall_score DECIMAL(5,2),
    f1_score DECIMAL(5,2),
    rmse DECIMAL(8,4),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dataset_size INTEGER,
    notes TEXT
);

-- Feature importance tracking
CREATE TABLE feature_importance (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    feature_name VARCHAR(50) NOT NULL,
    importance_score DECIMAL(8,6),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log for tracking all database changes
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System configuration
CREATE TABLE system_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_loan_applications_user_id ON loan_applications(user_id);
CREATE INDEX idx_loan_applications_status ON loan_applications(status);
CREATE INDEX idx_loan_applications_date ON loan_applications(application_date);
CREATE INDEX idx_predictions_application_id ON predictions(application_id);
CREATE INDEX idx_predictions_final_prediction ON predictions(final_prediction);
CREATE INDEX idx_predictions_date ON predictions(prediction_date);
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_model_performance_name_date ON model_performance(model_name, evaluation_date);

-- Insert default system configuration
INSERT INTO system_config (config_key, config_value, description) VALUES
('model_version', '1.0', 'Current ML model version'),
('min_credit_score', '300', 'Minimum acceptable credit score'),
('max_credit_score', '850', 'Maximum credit score'),
('default_confidence_threshold', '0.75', 'Minimum confidence for auto-approval'),
('max_loan_amount', '500000', 'Maximum loan amount allowed'),
('system_maintenance_mode', 'false', 'System maintenance status');

-- Insert sample model performance data
INSERT INTO model_performance (model_name, accuracy, precision_score, recall_score, f1_score, rmse, dataset_size, notes) VALUES
('XGBoost', 94.50, 0.92, 0.91, 0.91, 0.234, 1000, 'Primary model with best performance'),
('Random Forest', 92.10, 0.89, 0.88, 0.88, 0.281, 1000, 'Ensemble model for validation'),
('Logistic Regression', 87.30, 0.85, 0.84, 0.84, 0.356, 1000, 'Baseline linear model'),
('K-Nearest Neighbors', 85.70, 0.83, 0.82, 0.82, 0.378, 1000, 'Distance-based classifier');

-- Insert feature importance data
INSERT INTO feature_importance (model_name, feature_name, importance_score) VALUES
('XGBoost', 'credit_short', 0.285),
('XGBoost', 'credit_long', 0.267),
('XGBoost', 'cph', 0.198),
('XGBoost', 'payment_history', 0.156),
('XGBoost', 'aph', 0.094),
('Random Forest', 'credit_short', 0.312),
('Random Forest', 'credit_long', 0.289),
('Random Forest', 'cph', 0.203),
('Random Forest', 'payment_history', 0.196);