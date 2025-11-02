#!/usr/bin/env python3
"""
Complete Database Setup Script for Loan Prediction System
This script sets up the entire database infrastructure
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = ['pandas', 'sqlite3', 'flask']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            elif package == 'pandas':
                import pandas
            elif package == 'flask':
                import flask
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing Python packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        # Install pandas and flask if missing
        if 'pandas' in missing_packages:
            run_command("pip install pandas openpyxl", "Installing pandas and openpyxl")
        if 'flask' in missing_packages:
            run_command("pip install flask flask-cors PyJWT", "Installing Flask and dependencies")
        
        return True
    else:
        print("✅ All required Python packages are available")
        return True

def setup_database():
    """Set up the SQLite database"""
    print("\n🗄️  Setting up SQLite Database...")
    
    # Import and run database setup
    try:
        from database.sqlite_setup import main as setup_main
        setup_main()
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("\n🧪 Testing Database Operations...")
    
    try:
        from database.database_manager import test_database_operations
        test_database_operations()
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def setup_backend():
    """Set up Flask backend"""
    print("\n🌐 Setting up Flask Backend...")
    
    # Check if backend directory exists
    if not os.path.exists('backend'):
        print("❌ Backend directory not found")
        return False
    
    # Install Python requirements if requirements.txt exists
    if os.path.exists('backend/requirements.txt'):
        success = run_command(
            "pip install -r backend/requirements.txt", 
            "Installing Python backend requirements"
        )
        if not success:
            print("⚠️  Some packages might not have installed correctly")
    
    return True

def create_env_file():
    """Create environment configuration file"""
    print("\n⚙️  Creating environment configuration...")
    
    env_content = """# Loan Prediction System Configuration

# Database Configuration
DATABASE_PATH=database/loan_prediction.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# API Configuration
API_HOST=localhost
API_PORT=5000

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000/api

# ML Model Configuration
MODEL_VERSION=1.0
CONFIDENCE_THRESHOLD=0.75
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment file created (.env)")
        return True
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n📜 Creating startup scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
# Start Flask Backend Server
echo "🚀 Starting Loan Prediction API Server..."
cd backend
python app.py
"""
    
    # Full system startup script
    full_script = """#!/bin/bash
# Start Full Loan Prediction System
echo "🚀 Starting Loan Prediction System..."

# Start backend in background
echo "📡 Starting API server..."
cd backend && python app.py &
BACKEND_PID=$!

# Start frontend
echo "🌐 Starting React frontend..."
cd ..
npm start &
FRONTEND_PID=$!

echo "✅ System started!"
echo "📡 API Server: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
    
    try:
        # Create backend startup script
        with open('start_backend.sh', 'w') as f:
            f.write(backend_script)
        os.chmod('start_backend.sh', 0o755)
        
        # Create full system startup script
        with open('start_system.sh', 'w') as f:
            f.write(full_script)
        os.chmod('start_system.sh', 0o755)
        
        print("✅ Startup scripts created:")
        print("   - start_backend.sh (API server only)")
        print("   - start_system.sh (Full system)")
        return True
    except Exception as e:
        print(f"❌ Failed to create startup scripts: {e}")
        return False

def print_summary():
    """Print setup summary and next steps"""
    print("\n" + "="*60)
    print("🎉 LOAN PREDICTION SYSTEM SETUP COMPLETE!")
    print("="*60)
    print("\n📁 Project Structure:")
    print("   ├── database/")
    print("   │   ├── loan_prediction.db     (SQLite database)")
    print("   │   ├── schema.sql             (Database schema)")
    print("   │   ├── sqlite_setup.py        (Database setup)")
    print("   │   └── database_manager.py    (Database operations)")
    print("   ├── backend/")
    print("   │   ├── app.py                 (Flask API server)")
    print("   │   └── requirements.txt       (Python dependencies)")
    print("   ├── src/")
    print("   │   └── pages/                 (React components)")
    print("   └── ML Models (XGBoost, Random Forest, etc.)")
    
    print("\n🚀 How to Start the System:")
    print("   1. Start API server:    ./start_backend.sh")
    print("   2. Start React app:     npm start")
    print("   3. Start full system:   ./start_system.sh")
    
    print("\n🌐 Access Points:")
    print("   • Frontend:  http://localhost:3000")
    print("   • API:       http://localhost:5000")
    print("   • Health:    http://localhost:5000/api/health")
    
    print("\n📊 Database Info:")
    print("   • Location:  database/loan_prediction.db")
    print("   • Type:      SQLite")
    print("   • Tables:    users, loan_applications, predictions, etc.")
    
    print("\n🔧 API Endpoints:")
    print("   • POST /api/predict              - Loan prediction")
    print("   • GET  /api/dashboard/stats      - Dashboard data")
    print("   • GET  /api/dashboard/trends     - Monthly trends")
    print("   • GET  /api/dashboard/performance - Model metrics")
    
    print("\n📝 Next Steps:")
    print("   1. Test the prediction API with your React frontend")
    print("   2. Load your Excel data using the database manager")
    print("   3. Integrate real ML models by replacing simulation")
    print("   4. Add user authentication for production use")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 LOAN PREDICTION SYSTEM DATABASE SETUP")
    print("="*50)
    
    success_count = 0
    total_steps = 6
    
    # Step 1: Check Python packages
    if check_python_packages():
        success_count += 1
    
    # Step 2: Set up database
    if setup_database():
        success_count += 1
    
    # Step 3: Test database
    if test_database():
        success_count += 1
    
    # Step 4: Set up backend
    if setup_backend():
        success_count += 1
    
    # Step 5: Create environment file
    if create_env_file():
        success_count += 1
    
    # Step 6: Create startup scripts
    if create_startup_scripts():
        success_count += 1
    
    # Print results
    print(f"\n📊 Setup Results: {success_count}/{total_steps} steps completed successfully")
    
    if success_count == total_steps:
        print_summary()
    else:
        print("⚠️  Some setup steps failed. Please check the errors above.")
        print("💡 You can run this script again to retry failed steps.")

if __name__ == "__main__":
    main()