#!/usr/bin/env python3
"""
Integration Test Suite for Loan Prediction System
Tests the complete frontend-backend-database integration
"""

import requests
import json
import time
import subprocess
import os
import sys
from pathlib import Path
import threading
from database.database_manager import DatabaseManager

class IntegrationTester:
    def __init__(self):
        self.api_base = "http://localhost:5000/api"
        self.frontend_url = "http://localhost:3000"
        self.backend_process = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            'name': test_name,
            'success': success,
            'message': message
        })
        print(f"{test_name:<30} {status} {message}")
    
    def start_backend_for_testing(self):
        """Start backend server for testing"""
        print("🚀 Starting backend server for testing...")
        
        try:
            backend_dir = Path('backend')
            self.backend_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Test if server is responding
            try:
                response = requests.get(f"{self.api_base}/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Backend server started successfully")
                    return True
            except:
                pass
            
            print("❌ Backend server failed to start properly")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def stop_backend(self):
        """Stop backend server"""
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
    
    def test_database_operations(self):
        """Test database operations"""
        print("\n🗄️  Testing Database Operations...")
        
        try:
            db = DatabaseManager()
            
            # Test basic connectivity
            stats = db.get_dashboard_stats()
            self.log_test("Database Connection", True, f"Connected successfully")
            
            # Test configuration
            version = db.get_config('model_version')
            self.log_test("Database Config", version is not None, f"Version: {version}")
            
            # Test model performance data
            performance = db.get_model_performance()
            self.log_test("Model Performance Data", len(performance) > 0, f"{len(performance)} records")
            
            return True
            
        except Exception as e:
            self.log_test("Database Operations", False, str(e))
            return False
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🌐 Testing API Endpoints...")
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            self.log_test("Health Endpoint", response.status_code == 200, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Health Endpoint", False, str(e))
        
        # Test dashboard stats
        try:
            response = requests.get(f"{self.api_base}/dashboard/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Dashboard Stats", True, 
                             f"Predictions: {data.get('total_predictions', 0)}")
            else:
                self.log_test("Dashboard Stats", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Dashboard Stats", False, str(e))
        
        # Test model performance
        try:
            response = requests.get(f"{self.api_base}/dashboard/performance", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Model Performance", True, f"{len(data)} models")
            else:
                self.log_test("Model Performance", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Model Performance", False, str(e))
        
        # Test feature importance
        try:
            response = requests.get(f"{self.api_base}/dashboard/feature-importance", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Feature Importance", True, f"{len(data)} features")
            else:
                self.log_test("Feature Importance", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Feature Importance", False, str(e))
    
    def test_prediction_api(self):
        """Test loan prediction API with various scenarios"""
        print("\n🔮 Testing Prediction API...")
        
        test_cases = [
            {
                "name": "High Credit Score",
                "data": {
                    "creditShort": 780,
                    "creditLong": 760,
                    "paymentHistory": "excellent",
                    "timeLimitation": 3,
                    "cph": 0.95,
                    "ctl": 0.85,
                    "aph": 0.92,
                    "atl": 0.88,
                    "quarterFluctuation": 2,
                    "residualFluctuation": 1
                },
                "expected": "Very_Good"
            },
            {
                "name": "Medium Credit Score",
                "data": {
                    "creditShort": 650,
                    "creditLong": 630,
                    "paymentHistory": "good",
                    "timeLimitation": 5,
                    "cph": 0.75,
                    "ctl": 0.70,
                    "aph": 0.78,
                    "atl": 0.72,
                    "quarterFluctuation": 4,
                    "residualFluctuation": 3
                },
                "expected": "Normal"
            },
            {
                "name": "Low Credit Score",
                "data": {
                    "creditShort": 520,
                    "creditLong": 500,
                    "paymentHistory": "poor",
                    "timeLimitation": 8,
                    "cph": 0.45,
                    "ctl": 0.40,
                    "aph": 0.50,
                    "atl": 0.42,
                    "quarterFluctuation": 8,
                    "residualFluctuation": 6
                },
                "expected": "Very_Bad"
            }
        ]
        
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{self.api_base}/predict",
                    json=test_case["data"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get('prediction')
                    confidence = result.get('confidence')
                    
                    # Check if prediction matches expected category
                    success = prediction == test_case["expected"]
                    message = f"Got: {prediction} ({confidence}%)"
                    
                    self.log_test(f"Prediction: {test_case['name']}", success, message)
                    
                    # Test response structure
                    required_fields = ['prediction', 'confidence', 'loan_range', 'factors']
                    has_all_fields = all(field in result for field in required_fields)
                    self.log_test(f"Response Structure: {test_case['name']}", 
                                has_all_fields, "All required fields present")
                    
                else:
                    self.log_test(f"Prediction: {test_case['name']}", False, 
                                f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Prediction: {test_case['name']}", False, str(e))
    
    def test_ml_models_integration(self):
        """Test ML models integration"""
        print("\n🤖 Testing ML Models Integration...")
        
        # Check if model files exist
        model_files = [
            'XGBoostModel.pkl',
            'RandomForestModel.pkl',
            'LogisticModel.pkl',
            'KNNModel.pkl'
        ]
        
        for model_file in model_files:
            exists = os.path.exists(model_file)
            self.log_test(f"Model File: {model_file}", exists, 
                         "Found" if exists else "Not found")
        
        # Test model loading through API
        try:
            # Make a prediction request to test model loading
            test_data = {
                "creditShort": 700,
                "creditLong": 680,
                "paymentHistory": "good",
                "cph": 0.8,
                "ctl": 0.75,
                "aph": 0.85,
                "atl": 0.78,
                "quarterFluctuation": 3,
                "residualFluctuation": 2
            }
            
            response = requests.post(f"{self.api_base}/predict", json=test_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                processing_time = result.get('processing_time_ms', 0)
                
                # Check if processing time is reasonable (< 5 seconds)
                fast_processing = processing_time < 5000
                self.log_test("ML Processing Speed", fast_processing, 
                             f"{processing_time}ms")
                
                # Check if model predictions are included
                has_model_predictions = 'model_predictions' in result
                self.log_test("Model Predictions Included", has_model_predictions,
                             "Individual model results available")
                
            else:
                self.log_test("ML Models Integration", False, 
                             f"Prediction failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("ML Models Integration", False, str(e))
    
    def test_frontend_backend_integration(self):
        """Test frontend-backend integration"""
        print("\n🔗 Testing Frontend-Backend Integration...")
        
        # Test CORS headers
        try:
            response = requests.options(f"{self.api_base}/predict", 
                                      headers={'Origin': 'http://localhost:3000'})
            
            cors_headers = response.headers.get('Access-Control-Allow-Origin')
            self.log_test("CORS Configuration", cors_headers is not None,
                         f"Origin: {cors_headers}")
            
        except Exception as e:
            self.log_test("CORS Configuration", False, str(e))
        
        # Test API response format for frontend
        try:
            test_data = {
                "creditShort": 720,
                "creditLong": 700,
                "paymentHistory": "excellent",
                "cph": 0.9,
                "ctl": 0.8,
                "aph": 0.9,
                "atl": 0.85,
                "quarterFluctuation": 2,
                "residualFluctuation": 1
            }
            
            response = requests.post(f"{self.api_base}/predict", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check frontend-expected fields
                frontend_fields = ['prediction', 'confidence', 'loan_range', 'factors']
                has_frontend_fields = all(field in result for field in frontend_fields)
                
                self.log_test("Frontend API Format", has_frontend_fields,
                             "All frontend fields present")
                
                # Check factors structure
                factors = result.get('factors', {})
                expected_factors = ['creditScore', 'paymentHistory', 'debtRatio']
                has_factors = all(factor in factors for factor in expected_factors)
                
                self.log_test("Factors Structure", has_factors,
                             "All factor fields present")
                
            else:
                self.log_test("Frontend API Format", False, 
                             f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Frontend API Format", False, str(e))
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n🚨 Testing Error Handling...")
        
        # Test invalid input
        try:
            invalid_data = {
                "creditShort": "invalid",
                "creditLong": -100,
                "paymentHistory": "unknown"
            }
            
            response = requests.post(f"{self.api_base}/predict", json=invalid_data)
            
            # Should handle gracefully (either 400 error or fallback prediction)
            handled_gracefully = response.status_code in [200, 400, 422]
            self.log_test("Invalid Input Handling", handled_gracefully,
                         f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("Invalid Input Handling", False, str(e))
        
        # Test missing fields
        try:
            incomplete_data = {
                "creditShort": 700
                # Missing required fields
            }
            
            response = requests.post(f"{self.api_base}/predict", json=incomplete_data)
            handled_gracefully = response.status_code in [200, 400, 422]
            self.log_test("Missing Fields Handling", handled_gracefully,
                         f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("Missing Fields Handling", False, str(e))
        
        # Test non-existent endpoint
        try:
            response = requests.get(f"{self.api_base}/nonexistent")
            is_404 = response.status_code == 404
            self.log_test("404 Error Handling", is_404, f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("404 Error Handling", False, str(e))
    
    def run_full_integration_test(self):
        """Run complete integration test suite"""
        print("🧪 LOAN PREDICTION SYSTEM INTEGRATION TEST")
        print("=" * 60)
        
        # Start backend server
        if not self.start_backend_for_testing():
            print("❌ Cannot start backend server for testing")
            return False
        
        try:
            # Run all test suites
            self.test_database_operations()
            self.test_api_endpoints()
            self.test_prediction_api()
            self.test_ml_models_integration()
            self.test_frontend_backend_integration()
            self.test_error_handling()
            
            # Calculate results
            total_tests = len(self.test_results)
            passed_tests = sum(1 for result in self.test_results if result['success'])
            
            print("\n" + "=" * 60)
            print("📊 INTEGRATION TEST RESULTS")
            print("=" * 60)
            
            for result in self.test_results:
                status = "✅" if result['success'] else "❌"
                print(f"{status} {result['name']:<35} {result['message']}")
            
            print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
            
            if passed_tests == total_tests:
                print("\n🎉 All integration tests passed!")
                print("✅ System is fully integrated and working correctly")
                return True
            else:
                print(f"\n⚠️  {total_tests - passed_tests} tests failed")
                print("💡 Check the failed tests above for issues to resolve")
                return False
                
        finally:
            self.stop_backend()

def main():
    """Main test function"""
    tester = IntegrationTester()
    success = tester.run_full_integration_test()
    
    if success:
        print("\n🚀 System is ready for use!")
        print("   • Start backend: python backend/app.py")
        print("   • Start frontend: npm start")
        print("   • Full system: python start_full_system.py")
    else:
        print("\n🔧 Please fix the failing tests before using the system")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)