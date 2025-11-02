#!/usr/bin/env python3
"""
Quick Start Script for Loan Prediction System
Run this file to start your project instantly
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_project_files():
    """Check if all necessary files exist"""
    required_files = [
        '../backend/app.py',
        '../package.json',
        '../database/loan_prediction.db'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        print("\n💡 Make sure you're in the correct project directory")
        return False
    
    return True

def start_backend():
    """Start the Flask backend"""
    print("🚀 Starting Backend Server...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, '../backend/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment to see if it starts successfully
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("✅ Backend started successfully on http://localhost:5000")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"Error: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("🌐 Starting Frontend Server...")
    try:
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            cwd='..',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("✅ Frontend starting... (will open in browser)")
        print("🌐 Frontend will be available at http://localhost:3000")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🚀 LOAN PREDICTION SYSTEM - QUICK START")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not check_project_files():
        print("\n💡 Navigate to your project directory and run this script again")
        return
    
    print("✅ All project files found")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start system without backend")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Frontend failed to start, but backend is running")
        print("🌐 You can still access the API at http://localhost:5000")
    
    # Print success message
    print("\n" + "=" * 50)
    print("🎉 SYSTEM STARTED SUCCESSFULLY!")
    print("=" * 50)
    print("\n🌐 Access Points:")
    print("   • Frontend:  http://localhost:3000")
    print("   • API:       http://localhost:5000")
    print("   • Health:    http://localhost:5000/api/health")
    
    print("\n🔧 Controls:")
    print("   • Press Ctrl+C to stop all services")
    
    # Keep the script running
    try:
        print("\n⏳ System running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
            
        print("✅ System stopped successfully")
        print("👋 Run this script again to restart!")

if __name__ == "__main__":
    main()