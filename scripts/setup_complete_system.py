#!/usr/bin/env python3
"""
Complete System Setup for Loan Prediction System
Sets up database, backend, frontend, and runs integration tests
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completed successfully")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False, e.stderr

def check_system_requirements():
    """Check if all system requirements are met"""
    print("🔍 Checking System Requirements...")
    
    requirements = []
    
    # Check Python
    try:
        import sys
        python_version = sys.version_info
        if python_version >= (3, 7):
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            requirements.append(True)
        else:
            print(f"❌ Python {python_version.major}.{python_version.minor} (need 3.7+)")
            requirements.append(False)
    except:
        print("❌ Python not found")
        requirements.append(False)
    
    # Check Node.js
    success, output = run_command("node --version", "Checking Node.js")
    if success:
        print(f"✅ Node.js {output.strip()}")
        requirements.append(True)
    else:
        print("❌ Node.js not found")
        requirements.append(False)
    
    # Check npm
    success, output = run_command("npm --version", "Checking npm")
    if success:
        print(f"✅ npm {output.strip()}")
        requirements.append(True)
    else:
        print("❌ npm not found")
        requirements.append(False)
    
    return all(requirements)

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python Dependencies...")
    
    # Core dependencies
    core_packages = [
        "flask>=2.3.0",
        "flask-cors>=4.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "PyJWT>=2.8.0",
        "openpyxl>=3.1.0"
    ]
    
    # ML dependencies (optional)
    ml_packages = [
        "scikit-learn>=1.3.0",
        "xgboost>=1.7.0",
        "joblib>=1.3.0"
    ]
    
    # Install core packages
    for package in core_packages:
        success, _ = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️  Failed to install {package}, continuing...")
    
    # Install ML packages (optional)
    print("\n🤖 Installing ML Dependencies (optional)...")
    for package in ml_packages:
        success, _ = run_command(f"pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️  Failed to install {package}, ML models may not work")
    
    return True

def install_frontend_dependencies():
    """Install React frontend dependencies"""
    print("\n🌐 Installing Frontend Dependencies...")
    
    if not Path("package.json").exists():
        print("❌ package.json not found")
        return False
    
    success, _ = run_command("npm install", "Installing React dependencies")
    return success

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting Up Database...")
    
    success, _ = run_command("python setup_database.py", "Setting up database")
    return success

def create_configuration():
    """Create system configuration"""
    print("\n⚙️  Creating Configuration...")
    
    success, _ = run_command("python config.py", "Creating configuration")
    return success

def run_system_tests():
    """Run system tests"""
    print("\n🧪 Running System Tests...")
    
    # Basic system test
    success, _ = run_command("python test_system.py", "Running basic tests")
    if not success:
        return False
    
    # Integration test
    success, _ = run_command("python test_integration.py", "Running integration tests")
    return success

def create_startup_scripts():
    """Create startup scripts"""
    print("\n📜 Creating Startup Scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
echo "🚀 Starting Loan Prediction Backend..."
cd backend
python app.py
"""
    
    # Frontend startup script  
    frontend_script = """#!/bin/bash
echo "🌐 Starting Loan Prediction Frontend..."
npm start
"""
    
    # Full system script
    full_script = """#!/bin/bash
echo "🚀 Starting Complete Loan Prediction System..."
python start_full_system.py
"""
    
    try:
        # Create scripts
        with open("start_backend.sh", "w") as f:
            f.write(backend_script)
        os.chmod("start_backend.sh", 0o755)
        
        with open("start_frontend.sh", "w") as f:
            f.write(frontend_script)
        os.chmod("start_frontend.sh", 0o755)
        
        with open("start_system.sh", "w") as f:
            f.write(full_script)
        os.chmod("start_system.sh", 0o755)
        
        print("✅ Startup scripts created")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create startup scripts: {e}")
        return False

def print_system_info():
    """Print system information and next steps"""
    print("\n" + "=" * 70)
    print("🎉 LOAN PREDICTION SYSTEM SETUP COMPLETE!")
    print("=" * 70)
    
    print("\n📁 Project Structure:")
    print("   ├── backend/")
    print("   │   ├── app.py                 (Flask API server)")
    print("   │   ├── ml_models.py           (ML model integration)")
    print("   │   └── requirements.txt       (Python dependencies)")
    print("   ├── database/")
    print("   │   ├── loan_prediction.db     (SQLite database)")
    print("   │   ├── schema.sql             (Database schema)")
    print("   │   ├── sqlite_setup.py        (Database setup)")
    print("   │   └── database_manager.py    (Database operations)")
    print("   ├── src/")
    print("   │   ├── pages/                 (React components)")
    print("   │   ├── services/              (API integration)")
    print("   │   └── components/            (UI components)")
    print("   ├── ML Models/")
    print("   │   ├── XGBoostModel.pkl       (Trained XGBoost model)")
    print("   │   ├── RandomForestModel.pkl  (Trained Random Forest)")
    print("   │   └── Other model files...")
    print("   └── Configuration & Scripts")
    
    print("\n🚀 How to Start the System:")
    print("   1. Backend only:     ./start_backend.sh")
    print("   2. Frontend only:    ./start_frontend.sh") 
    print("   3. Complete system:  ./start_system.sh")
    print("   4. Python launcher:  python start_full_system.py")
    
    print("\n🌐 Access Points:")
    print("   • Frontend:    http://localhost:3000")
    print("   • API:         http://localhost:5000")
    print("   • Health:      http://localhost:5000/api/health")
    print("   • Dashboard:   http://localhost:3000/dashboard")
    print("   • Prediction:  http://localhost:3000/predict")
    
    print("\n🔧 API Endpoints:")
    print("   • POST /api/predict              - Loan prediction")
    print("   • GET  /api/dashboard/stats      - Dashboard statistics")
    print("   • GET  /api/dashboard/performance - Model performance")
    print("   • GET  /api/dashboard/trends     - Monthly trends")
    print("   • GET  /api/health               - Health check")
    
    print("\n📊 Features:")
    print("   ✅ AI-powered loan predictions (4 ML models)")
    print("   ✅ Real-time dashboard with analytics")
    print("   ✅ SQLite database with complete schema")
    print("   ✅ React frontend with modern UI")
    print("   ✅ Flask REST API backend")
    print("   ✅ Model performance tracking")
    print("   ✅ Feature importance analysis")
    print("   ✅ Error handling and fallbacks")
    
    print("\n🧪 Testing:")
    print("   • Basic tests:       python test_system.py")
    print("   • Integration tests: python test_integration.py")
    print("   • Health check:      curl http://localhost:5000/api/health")
    
    print("\n📝 Next Steps:")
    print("   1. Start the system using one of the startup methods above")
    print("   2. Open http://localhost:3000 in your browser")
    print("   3. Try the loan prediction feature")
    print("   4. Explore the dashboard analytics")
    print("   5. Check the About page for system information")
    
    print("\n🔧 Troubleshooting:")
    print("   • Check logs in terminal for errors")
    print("   • Ensure ports 3000 and 5000 are available")
    print("   • Run tests to verify system health")
    print("   • Check database file exists: database/loan_prediction.db")
    
    print("\n" + "=" * 70)

def main():
    """Main setup function"""
    print("🚀 LOAN PREDICTION SYSTEM COMPLETE SETUP")
    print("=" * 50)
    
    setup_steps = [
        ("System Requirements", check_system_requirements),
        ("Python Dependencies", install_python_dependencies),
        ("Frontend Dependencies", install_frontend_dependencies),
        ("Database Setup", setup_database),
        ("Configuration", create_configuration),
        ("Startup Scripts", create_startup_scripts),
        ("System Tests", run_system_tests)
    ]
    
    results = []
    
    for step_name, step_function in setup_steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            success = step_function()
            results.append((step_name, success))
            
            if success:
                print(f"✅ {step_name} completed successfully")
            else:
                print(f"❌ {step_name} failed")
                
        except Exception as e:
            print(f"💥 {step_name} failed with error: {e}")
            results.append((step_name, False))
    
    # Print results summary
    print(f"\n{'='*20} SETUP SUMMARY {'='*20}")
    
    total_steps = len(results)
    successful_steps = sum(1 for _, success in results if success)
    
    for step_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {step_name}")
    
    print(f"\n📊 Results: {successful_steps}/{total_steps} steps completed successfully")
    
    if successful_steps == total_steps:
        print("\n🎉 Complete setup successful!")
        print_system_info()
        
        # Ask if user wants to start the system
        try:
            response = input("\n❓ Start the complete system now? (y/n): ")
            if response.lower() == 'y':
                print("\n🚀 Starting system...")
                os.system("python start_full_system.py")
        except KeyboardInterrupt:
            print("\n👋 Setup complete. Start system manually when ready.")
            
    else:
        failed_steps = [name for name, success in results if not success]
        print(f"\n⚠️  Setup partially completed. Failed steps: {', '.join(failed_steps)}")
        print("💡 You can still use the system, but some features may not work properly.")
        print("🔧 Try running the failed steps manually or check the error messages above.")

if __name__ == "__main__":
    main()