#!/usr/bin/env python3
"""
System Test Script for Loan Prediction System
Tests database connectivity and API functionality
"""

import requests
import json
import time
from database.database_manager import DatabaseManager

def test_database():
    """Test database operations"""
    print("🗄️  Testing Database...")
    
    try:
        db = DatabaseManager()
        
        # Test basic connectivity
        stats = db.get_dashboard_stats()
        print(f"✅ Database connected successfully")
        print(f"📊 Total predictions: {stats.get('total_predictions', 0)}")
        
        # Test model performance data
        performance = db.get_model_performance()
        print(f"🎯 Model performance records: {len(performance)}")
        
        # Test feature importance
        importance = db.get_feature_importance('XGBoost')
        print(f"📈 XGBoost features: {len(importance)}")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_api_health():
    """Test API health endpoint"""
    print("\n🌐 Testing API Health...")
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy")
            print(f"📡 Status: {data.get('status')}")
            print(f"🕐 Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running")
        return False
    except Exception as e:
        print(f"❌ API health test failed: {e}")
        return False

def test_prediction_api():
    """Test loan prediction API"""
    print("\n🔮 Testing Prediction API...")
    
    # Sample prediction data
    test_data = {
        "creditShort": 720,
        "creditLong": 700,
        "paymentHistory": "good",
        "timeLimitation": 5,
        "cph": 0.85,
        "ctl": 0.75,
        "aph": 0.90,
        "atl": 0.80,
        "quarterFluctuation": 3,
        "residualFluctuation": 2,
        "requestedAmount": 75000,
        "loanPurpose": "Home Purchase",
        "employmentStatus": "Employed",
        "annualIncome": 85000
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/predict',
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction API working")
            print(f"🎯 Prediction: {data.get('prediction')}")
            print(f"📊 Confidence: {data.get('confidence')}%")
            print(f"💰 Loan Range: {data.get('loan_range')}")
            print(f"⏱️  Processing Time: {data.get('processing_time_ms')}ms")
            return True
        else:
            print(f"❌ Prediction API failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction API test failed: {e}")
        return False

def test_dashboard_api():
    """Test dashboard API endpoints"""
    print("\n📊 Testing Dashboard API...")
    
    endpoints = [
        ('/api/dashboard/stats', 'Dashboard Stats'),
        ('/api/dashboard/performance', 'Model Performance'),
        ('/api/dashboard/feature-importance', 'Feature Importance')
    ]
    
    success_count = 0
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name}: {len(data) if isinstance(data, list) else 'OK'}")
                success_count += 1
            else:
                print(f"❌ {name} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    return success_count == len(endpoints)

def create_sample_data():
    """Create some sample data for testing"""
    print("\n📝 Creating Sample Data...")
    
    try:
        db = DatabaseManager()
        
        # Create sample loan applications
        sample_applications = [
            {
                'credit_short': 750, 'credit_long': 720, 'payment_history': 'excellent',
                'cph': 0.9, 'ctl': 0.8, 'aph': 0.95, 'atl': 0.85,
                'quarter_fluctuation': 2, 'residual_fluctuation': 1,
                'requested_amount': 100000, 'loan_purpose': 'Home Purchase',
                'employment_status': 'Employed', 'annual_income': 95000
            },
            {
                'credit_short': 650, 'credit_long': 630, 'payment_history': 'good',
                'cph': 0.75, 'ctl': 0.7, 'aph': 0.8, 'atl': 0.75,
                'quarter_fluctuation': 4, 'residual_fluctuation': 3,
                'requested_amount': 50000, 'loan_purpose': 'Car Purchase',
                'employment_status': 'Employed', 'annual_income': 65000
            },
            {
                'credit_short': 580, 'credit_long': 560, 'payment_history': 'fair',
                'cph': 0.6, 'ctl': 0.55, 'aph': 0.65, 'atl': 0.6,
                'quarter_fluctuation': 6, 'residual_fluctuation': 5,
                'requested_amount': 25000, 'loan_purpose': 'Personal',
                'employment_status': 'Part-time', 'annual_income': 35000
            }
        ]
        
        for i, app_data in enumerate(sample_applications):
            # Create application
            app_id = db.create_loan_application(1, app_data)  # user_id = 1 (demo user)
            
            # Create corresponding prediction
            if app_data['credit_short'] > 700:
                prediction = 'Very_Good'
                confidence = 92.5
            elif app_data['credit_short'] > 600:
                prediction = 'Normal'
                confidence = 78.3
            else:
                prediction = 'Very_Bad'
                confidence = 65.1
            
            pred_data = {
                'xgboost_prediction': prediction,
                'xgboost_confidence': confidence,
                'random_forest_prediction': prediction,
                'random_forest_confidence': confidence - 2,
                'final_prediction': prediction,
                'final_confidence': confidence,
                'processing_time_ms': 150 + i * 20
            }
            
            db.save_prediction(app_id, pred_data)
            db.update_application_status(app_id, 'processed')
        
        print(f"✅ Created {len(sample_applications)} sample applications")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def run_full_test():
    """Run complete system test"""
    print("🚀 LOAN PREDICTION SYSTEM TEST")
    print("="*50)
    
    test_results = []
    
    # Test 1: Database
    test_results.append(("Database", test_database()))
    
    # Test 2: Create sample data
    test_results.append(("Sample Data", create_sample_data()))
    
    # Test 3: API Health
    test_results.append(("API Health", test_api_health()))
    
    # Test 4: Prediction API
    test_results.append(("Prediction API", test_prediction_api()))
    
    # Test 5: Dashboard API
    test_results.append(("Dashboard API", test_dashboard_api()))
    
    # Print results
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Start the Flask API: python backend/app.py")
        print("   2. Start the React app: npm start")
        print("   3. Open http://localhost:3000 in your browser")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Common solutions:")
        print("   - Make sure Flask server is running: python backend/app.py")
        print("   - Check database permissions and file paths")
        print("   - Verify all Python dependencies are installed")

if __name__ == "__main__":
    run_full_test()