#!/usr/bin/env python3
"""
Database Manager for Loan Prediction System
Provides high-level database operations and utilities
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class DatabaseManager:
    def __init__(self, db_path="database/loan_prediction.db"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a SELECT query and return results as list of dictionaries"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE query and return affected rows"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return affected_rows
    
    # User Management
    def create_user(self, username: str, email: str, password_hash: str, 
                   first_name: str = None, last_name: str = None) -> int:
        """Create a new user and return user ID"""
        query = """
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (username, email, password_hash, first_name, last_name))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = ? AND is_active = 1"
        results = self.execute_query(query, (email,))
        return results[0] if results else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = ? AND is_active = 1"
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    # Loan Application Management
    def create_loan_application(self, user_id: int, application_data: Dict) -> int:
        """Create a new loan application"""
        query = """
            INSERT INTO loan_applications 
            (user_id, credit_short, credit_long, payment_history, time_limitation,
             cph, ctl, aph, atl, quarter_fluctuation, residual_fluctuation,
             requested_amount, loan_purpose, employment_status, annual_income)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            user_id,
            application_data.get('credit_short'),
            application_data.get('credit_long'),
            application_data.get('payment_history'),
            application_data.get('time_limitation'),
            application_data.get('cph'),
            application_data.get('ctl'),
            application_data.get('aph'),
            application_data.get('atl'),
            application_data.get('quarter_fluctuation'),
            application_data.get('residual_fluctuation'),
            application_data.get('requested_amount'),
            application_data.get('loan_purpose'),
            application_data.get('employment_status'),
            application_data.get('annual_income')
        )
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        app_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return app_id
    
    def get_loan_application(self, app_id: int) -> Optional[Dict]:
        """Get loan application by ID"""
        query = """
            SELECT la.*, u.username, u.email, u.first_name, u.last_name
            FROM loan_applications la
            JOIN users u ON la.user_id = u.id
            WHERE la.id = ?
        """
        results = self.execute_query(query, (app_id,))
        return results[0] if results else None
    
    def get_user_applications(self, user_id: int) -> List[Dict]:
        """Get all applications for a user"""
        query = """
            SELECT la.*, p.final_prediction, p.final_confidence
            FROM loan_applications la
            LEFT JOIN predictions p ON la.id = p.application_id
            WHERE la.user_id = ?
            ORDER BY la.application_date DESC
        """
        return self.execute_query(query, (user_id,))
    
    def update_application_status(self, app_id: int, status: str) -> bool:
        """Update application status"""
        query = "UPDATE loan_applications SET status = ? WHERE id = ?"
        affected = self.execute_update(query, (status, app_id))
        return affected > 0
    
    # Prediction Management
    def save_prediction(self, application_id: int, prediction_data: Dict) -> int:
        """Save ML model prediction"""
        query = """
            INSERT INTO predictions 
            (application_id, xgboost_prediction, xgboost_confidence,
             random_forest_prediction, random_forest_confidence,
             logistic_prediction, logistic_confidence,
             knn_prediction, knn_confidence,
             final_prediction, final_confidence, model_version, processing_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            application_id,
            prediction_data.get('xgboost_prediction'),
            prediction_data.get('xgboost_confidence'),
            prediction_data.get('random_forest_prediction'),
            prediction_data.get('random_forest_confidence'),
            prediction_data.get('logistic_prediction'),
            prediction_data.get('logistic_confidence'),
            prediction_data.get('knn_prediction'),
            prediction_data.get('knn_confidence'),
            prediction_data.get('final_prediction'),
            prediction_data.get('final_confidence'),
            prediction_data.get('model_version', '1.0'),
            prediction_data.get('processing_time_ms')
        )
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        pred_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return pred_id
    
    def get_prediction(self, application_id: int) -> Optional[Dict]:
        """Get prediction for an application"""
        query = "SELECT * FROM predictions WHERE application_id = ?"
        results = self.execute_query(query, (application_id,))
        return results[0] if results else None
    
    # Analytics and Reporting
    def get_dashboard_stats(self) -> Dict:
        """Get statistics for dashboard"""
        stats = {}
        
        # Total predictions
        query = "SELECT COUNT(*) as total FROM predictions"
        result = self.execute_query(query)
        stats['total_predictions'] = result[0]['total']
        
        # Approval rate
        query = """
            SELECT 
                COUNT(CASE WHEN final_prediction = 'Very_Good' THEN 1 END) * 100.0 / COUNT(*) as approval_rate
            FROM predictions
        """
        result = self.execute_query(query)
        stats['approval_rate'] = round(result[0]['approval_rate'], 1) if result[0]['approval_rate'] else 0
        
        # Average confidence
        query = "SELECT AVG(final_confidence) as avg_confidence FROM predictions"
        result = self.execute_query(query)
        stats['avg_confidence'] = round(result[0]['avg_confidence'], 1) if result[0]['avg_confidence'] else 0
        
        # Active users (users with applications in last 30 days)
        query = """
            SELECT COUNT(DISTINCT user_id) as active_users 
            FROM loan_applications 
            WHERE application_date >= datetime('now', '-30 days')
        """
        result = self.execute_query(query)
        stats['active_users'] = result[0]['active_users']
        
        # Prediction distribution
        query = """
            SELECT final_prediction, COUNT(*) as count
            FROM predictions
            GROUP BY final_prediction
        """
        distribution = self.execute_query(query)
        stats['prediction_distribution'] = {row['final_prediction']: row['count'] for row in distribution}
        
        return stats
    
    def get_monthly_trends(self, months: int = 6) -> List[Dict]:
        """Get monthly prediction trends"""
        query = """
            SELECT 
                strftime('%Y-%m', p.prediction_date) as month,
                COUNT(*) as total_predictions,
                COUNT(CASE WHEN p.final_prediction = 'Very_Good' THEN 1 END) as approvals
            FROM predictions p
            WHERE p.prediction_date >= datetime('now', '-{} months')
            GROUP BY strftime('%Y-%m', p.prediction_date)
            ORDER BY month
        """.format(months)
        
        return self.execute_query(query)
    
    def get_model_performance(self) -> List[Dict]:
        """Get latest model performance metrics"""
        query = """
            SELECT * FROM model_performance 
            ORDER BY evaluation_date DESC
            LIMIT 10
        """
        return self.execute_query(query)
    
    def get_feature_importance(self, model_name: str = None) -> List[Dict]:
        """Get feature importance data"""
        if model_name:
            query = """
                SELECT * FROM feature_importance 
                WHERE model_name = ?
                ORDER BY importance_score DESC
            """
            return self.execute_query(query, (model_name,))
        else:
            query = """
                SELECT * FROM feature_importance 
                ORDER BY model_name, importance_score DESC
            """
            return self.execute_query(query)
    
    # Configuration Management
    def get_config(self, key: str) -> Optional[str]:
        """Get configuration value"""
        query = "SELECT config_value FROM system_config WHERE config_key = ?"
        results = self.execute_query(query, (key,))
        return results[0]['config_value'] if results else None
    
    def set_config(self, key: str, value: str, description: str = None) -> bool:
        """Set configuration value"""
        query = """
            INSERT OR REPLACE INTO system_config (config_key, config_value, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """
        affected = self.execute_update(query, (key, value, description))
        return affected > 0
    
    # Data Export/Import
    def export_to_csv(self, table_name: str, output_path: str) -> bool:
        """Export table data to CSV"""
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.get_connection())
            df.to_csv(output_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting {table_name}: {e}")
            return False
    
    def backup_database(self, backup_path: str) -> bool:
        """Create database backup"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

# Example usage and testing
def test_database_operations():
    """Test database operations"""
    db = DatabaseManager()
    
    print("🧪 Testing Database Operations...")
    
    # Test dashboard stats
    stats = db.get_dashboard_stats()
    print(f"📊 Dashboard Stats: {stats}")
    
    # Test model performance
    performance = db.get_model_performance()
    print(f"🎯 Model Performance Records: {len(performance)}")
    
    # Test feature importance
    importance = db.get_feature_importance('XGBoost')
    print(f"📈 XGBoost Feature Importance: {len(importance)} features")
    
    # Test configuration
    version = db.get_config('model_version')
    print(f"⚙️ Model Version: {version}")
    
    print("✅ Database operations test completed!")

if __name__ == "__main__":
    test_database_operations()