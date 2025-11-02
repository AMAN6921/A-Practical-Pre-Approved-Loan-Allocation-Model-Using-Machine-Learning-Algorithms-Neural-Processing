#!/usr/bin/env python3
"""
SQLite Database Setup for Loan Prediction System
This script creates and initializes the SQLite database for development
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime
import hashlib

class LoanPredictionDB:
    def __init__(self, db_path="database/loan_prediction.db"):
        self.db_path = db_path
        self.ensure_directory()
        
    def ensure_directory(self):
        """Create database directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def create_database(self):
        """Create the SQLite database with all tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read and execute schema (modified for SQLite)
        schema_sql = self.get_sqlite_schema()
        
        # Execute each statement separately
        statements = schema_sql.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        conn.close()
        print(f"✅ Database created successfully at {self.db_path}")
    
    def get_sqlite_schema(self):
        """SQLite-compatible schema"""
        return """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        );

        -- Loan applications table
        CREATE TABLE IF NOT EXISTS loan_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            
            -- Financial features
            credit_short REAL NOT NULL,
            credit_long REAL NOT NULL,
            payment_history TEXT NOT NULL CHECK (payment_history IN ('excellent', 'good', 'fair', 'poor')),
            time_limitation REAL,
            cph REAL NOT NULL CHECK (cph BETWEEN 0 AND 1),
            ctl REAL NOT NULL CHECK (ctl BETWEEN 0 AND 1),
            aph REAL NOT NULL CHECK (aph BETWEEN 0 AND 1),
            atl REAL NOT NULL CHECK (atl BETWEEN 0 AND 1),
            quarter_fluctuation INTEGER,
            residual_fluctuation INTEGER,
            
            -- Application metadata
            application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processed', 'approved', 'rejected')),
            
            -- Additional details
            requested_amount REAL,
            loan_purpose TEXT,
            employment_status TEXT,
            annual_income REAL,
            
            CHECK (credit_short >= 0 AND credit_long >= 0)
        );

        -- Predictions table
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER REFERENCES loan_applications(id) ON DELETE CASCADE,
            
            -- Model predictions
            xgboost_prediction TEXT CHECK (xgboost_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR xgboost_prediction IS NULL),
            xgboost_confidence REAL,
            random_forest_prediction TEXT CHECK (random_forest_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR random_forest_prediction IS NULL),
            random_forest_confidence REAL,
            logistic_prediction TEXT CHECK (logistic_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR logistic_prediction IS NULL),
            logistic_confidence REAL,
            knn_prediction TEXT CHECK (knn_prediction IN ('Very_Good', 'Normal', 'Very_Bad') OR knn_prediction IS NULL),
            knn_confidence REAL,
            
            -- Final prediction
            final_prediction TEXT NOT NULL CHECK (final_prediction IN ('Very_Good', 'Normal', 'Very_Bad')),
            final_confidence REAL NOT NULL,
            prediction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            -- Metadata
            model_version TEXT DEFAULT '1.0',
            processing_time_ms INTEGER
        );

        -- Model performance tracking
        CREATE TABLE IF NOT EXISTS model_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            accuracy REAL,
            precision_score REAL,
            recall_score REAL,
            f1_score REAL,
            rmse REAL,
            evaluation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            dataset_size INTEGER,
            notes TEXT
        );

        -- Feature importance
        CREATE TABLE IF NOT EXISTS feature_importance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            feature_name TEXT NOT NULL,
            importance_score REAL,
            evaluation_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- System configuration
        CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key TEXT UNIQUE NOT NULL,
            config_value TEXT NOT NULL,
            description TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_loan_applications_user_id ON loan_applications(user_id);
        CREATE INDEX IF NOT EXISTS idx_loan_applications_status ON loan_applications(status);
        CREATE INDEX IF NOT EXISTS idx_predictions_application_id ON predictions(application_id);
        CREATE INDEX IF NOT EXISTS idx_predictions_final_prediction ON predictions(final_prediction);
        """
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert sample user
        password_hash = hashlib.sha256("demo123".encode()).hexdigest()
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, ("demo_user", "demo@example.com", password_hash, "Demo", "User"))
        
        # Insert system configuration
        config_data = [
            ('model_version', '1.0', 'Current ML model version'),
            ('min_credit_score', '300', 'Minimum acceptable credit score'),
            ('max_credit_score', '850', 'Maximum credit score'),
            ('default_confidence_threshold', '0.75', 'Minimum confidence for auto-approval'),
            ('max_loan_amount', '500000', 'Maximum loan amount allowed'),
            ('system_maintenance_mode', 'false', 'System maintenance status')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO system_config (config_key, config_value, description)
            VALUES (?, ?, ?)
        """, config_data)
        
        # Insert model performance data
        performance_data = [
            ('XGBoost', 94.50, 0.92, 0.91, 0.91, 0.234, 1000, 'Primary model with best performance'),
            ('Random Forest', 92.10, 0.89, 0.88, 0.88, 0.281, 1000, 'Ensemble model for validation'),
            ('Logistic Regression', 87.30, 0.85, 0.84, 0.84, 0.356, 1000, 'Baseline linear model'),
            ('K-Nearest Neighbors', 85.70, 0.83, 0.82, 0.82, 0.378, 1000, 'Distance-based classifier')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO model_performance 
            (model_name, accuracy, precision_score, recall_score, f1_score, rmse, dataset_size, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, performance_data)
        
        # Insert feature importance data
        importance_data = [
            ('XGBoost', 'credit_short', 0.285),
            ('XGBoost', 'credit_long', 0.267),
            ('XGBoost', 'cph', 0.198),
            ('XGBoost', 'payment_history', 0.156),
            ('XGBoost', 'aph', 0.094),
            ('Random Forest', 'credit_short', 0.312),
            ('Random Forest', 'credit_long', 0.289),
            ('Random Forest', 'cph', 0.203),
            ('Random Forest', 'payment_history', 0.196)
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO feature_importance (model_name, feature_name, importance_score)
            VALUES (?, ?, ?)
        """, importance_data)
        
        conn.commit()
        conn.close()
        print("✅ Sample data inserted successfully")
    
    def load_excel_data(self, excel_path="FINAL_DATASET_ARRANGED_MP2024.xlsx"):
        """Load data from Excel file into database"""
        if not os.path.exists(excel_path):
            print(f"❌ Excel file not found: {excel_path}")
            return
        
        try:
            # Read Excel data
            df = pd.read_excel(excel_path)
            print(f"📊 Loaded {len(df)} records from Excel file")
            print(f"📋 Columns: {list(df.columns)}")
            
            conn = sqlite3.connect(self.db_path)
            
            # Insert sample applications based on Excel data
            for index, row in df.iterrows():
                cursor = conn.cursor()
                
                # Create a sample loan application
                cursor.execute("""
                    INSERT INTO loan_applications 
                    (user_id, credit_short, credit_long, payment_history, cph, ctl, aph, atl, 
                     quarter_fluctuation, residual_fluctuation, requested_amount, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    1,  # demo user
                    float(row.get('Credit-Short', 0)),
                    float(row.get('Credit-Long', 0)),
                    'good',  # default payment history
                    0.8,     # default cph
                    0.7,     # default ctl
                    0.85,    # default aph
                    0.75,    # default atl
                    5,       # default quarter fluctuation
                    2,       # default residual fluctuation
                    50000,   # default requested amount
                    'processed'
                ))
                
                app_id = cursor.lastrowid
                
                # Create corresponding prediction
                cust_type = row.get('Cust_Type', 'Normal')
                confidence = 85.0 + (index % 15)  # Simulate varying confidence
                
                cursor.execute("""
                    INSERT INTO predictions 
                    (application_id, xgboost_prediction, xgboost_confidence, 
                     final_prediction, final_confidence, processing_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    app_id,
                    cust_type,
                    confidence,
                    cust_type,
                    confidence,
                    150 + (index % 100)  # Simulate processing time
                ))
            
            conn.commit()
            conn.close()
            print(f"✅ Successfully loaded {len(df)} records into database")
            
        except Exception as e:
            print(f"❌ Error loading Excel data: {e}")
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        tables = ['users', 'loan_applications', 'predictions', 'model_performance', 'feature_importance']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        
        # Get prediction distribution
        cursor.execute("""
            SELECT final_prediction, COUNT(*) 
            FROM predictions 
            GROUP BY final_prediction
        """)
        stats['prediction_distribution'] = dict(cursor.fetchall())
        
        conn.close()
        return stats

def main():
    """Main setup function"""
    print("🚀 Setting up Loan Prediction Database...")
    
    db = LoanPredictionDB()
    
    # Create database
    db.create_database()
    
    # Insert sample data
    db.insert_sample_data()
    
    # Load Excel data if available
    db.load_excel_data()
    
    # Show statistics
    stats = db.get_stats()
    print("\n📊 Database Statistics:")
    for table, count in stats.items():
        if table != 'prediction_distribution':
            print(f"   {table}: {count} records")
    
    if 'prediction_distribution' in stats:
        print("\n🎯 Prediction Distribution:")
        for pred, count in stats['prediction_distribution'].items():
            print(f"   {pred}: {count}")
    
    print(f"\n✅ Database setup complete! Database location: {db.db_path}")

if __name__ == "__main__":
    main()