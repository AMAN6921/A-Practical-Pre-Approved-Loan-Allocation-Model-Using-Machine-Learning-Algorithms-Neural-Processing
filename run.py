#!/usr/bin/env python3
"""
Simple Python script to run PALP AI system
Works on all platforms (Windows, macOS, Linux)
"""

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

def print_header():
    """Print fancy header"""
    print("\n" + "="*80)
    print("🌾 PALP AI - PRE-APPROVED LOAN PREDICTION 🌾".center(80))
    print("="*80 + "\n")

def check_models():
    """Check if models are trained, if not train them"""
    models_dir = Path("models")
    model_files = [
        "XGBoostModel.pkl",
        "RandomForestModel.pkl",
        "LogisticModel.pkl",
        "KNNModel.pkl",
        "MLPClassifierModel.pkl"
    ]
    
    all_exist = all((models_dir / f).exists() for f in model_files)
    
    if not all_exist:
        print("📦 Training ML models (first time only)...")
        print("   This will take 1-2 minutes...\n")
        
        model_scripts = [
            "XGBoostModel.py",
            "RandomForestModel.py",
            "LogisticModel.py",
            "KNNModel.py",
            "MultiLayerPerceptronTwoHiddenLayers.py"
        ]
        
        for script in model_scripts:
            print(f"   Training {script.replace('.py', '')}...")
            try:
                subprocess.run(
                    [sys.executable, script],
                    cwd="models",
                    capture_output=True,
                    timeout=120
                )
            except Exception as e:
                print(f"   ⚠️  Warning: {script} training had issues: {e}")
        
        print("\n✅ Models trained!\n")
    else:
        print("✅ ML models already trained\n")

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    # Start backend in background
    process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    print("   Waiting for server to start...")
    time.sleep(3)
    
    # Check if server is running
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:5000/api/health", timeout=5)
        print("✅ Backend running on http://localhost:5000\n")
        return process
    except:
        print("❌ Failed to start backend server\n")
        process.kill()
        return None

def open_demo():
    """Open the demo interface"""
    print("🎨 Opening demo interface...")
    demo_path = Path("frontend/index.html").absolute()
    webbrowser.open(f"file://{demo_path}")
    print("✅ Demo opened in browser\n")

def main():
    """Main function"""
    print_header()
    
    # Check and train models if needed
    check_models()
    
    # Start backend
    backend_process = start_backend()
    
    if not backend_process:
        print("❌ Failed to start system")
        return 1
    
    # Open demo
    open_demo()
    
    # Print status
    print("="*80)
    print("✅ SYSTEM IS RUNNING!".center(80))
    print("="*80 + "\n")
    print("🌐 Backend API:  http://localhost:5000")
    print("🎨 Demo UI:      Opened in your browser")
    print("🏥 Health Check: http://localhost:5000/api/health")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("="*80 + "\n")
    
    # Keep running
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping server...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped. Goodbye!\n")
        return 0

if __name__ == "__main__":
    sys.exit(main())
