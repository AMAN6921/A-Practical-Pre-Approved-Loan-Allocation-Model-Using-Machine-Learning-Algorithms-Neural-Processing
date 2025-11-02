#!/usr/bin/env python3
"""
Full System Startup Script for Loan Prediction System
Starts both backend and frontend with proper error handling
"""

import subprocess
import time
import os
import sys
import signal
import threading
from pathlib import Path

class SystemManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def check_dependencies(self):
        """Check if all dependencies are available"""
        print("🔍 Checking system dependencies...")
        
        # Check Python
        try:
            import flask, pandas, sqlite3
            print("✅ Python dependencies available")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("💡 Run: pip install flask flask-cors pandas PyJWT")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Node.js and npm available")
            else:
                print("❌ npm not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js/npm not found")
            print("💡 Install Node.js from https://nodejs.org/")
            return False
        
        # Check if React dependencies are installed
        if not os.path.exists('node_modules'):
            print("📦 Installing React dependencies...")
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ npm install failed: {result.stderr}")
                return False
            print("✅ React dependencies installed")
        
        return True
    
    def setup_database(self):
        """Ensure database is set up"""
        print("🗄️  Checking database setup...")
        
        if not os.path.exists('database/loan_prediction.db'):
            print("📊 Setting up database...")
            try:
                subprocess.run([sys.executable, 'setup_database.py'], check=True)
                print("✅ Database setup completed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Database setup failed: {e}")
                return False
        else:
            print("✅ Database already exists")
        
        return True
    
    def start_backend(self):
        """Start Flask backend server"""
        print("🚀 Starting Flask backend server...")
        
        try:
            # Change to backend directory
            backend_dir = Path('backend')
            if not backend_dir.exists():
                print("❌ Backend directory not found")
                return False
            
            # Start Flask app
            self.backend_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if process is still running
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully")
                print("📡 API available at: http://localhost:5000")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend failed to start:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start React frontend server"""
        print("🌐 Starting React frontend server...")
        
        try:
            # Start React development server
            self.frontend_process = subprocess.Popen(
                ['npm', 'start'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for React to start
            time.sleep(5)
            
            # Check if process is still running
            if self.frontend_process.poll() is None:
                print("✅ Frontend server started successfully")
                print("🌐 Frontend available at: http://localhost:3000")
                return True
            else:
                stdout, stderr = self.frontend_process.communicate()
                print(f"❌ Frontend failed to start:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor both processes and restart if needed"""
        while self.running:
            time.sleep(5)
            
            # Check backend
            if self.backend_process and self.backend_process.poll() is not None:
                print("⚠️  Backend process died, restarting...")
                self.start_backend()
            
            # Check frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("⚠️  Frontend process died, restarting...")
                self.start_frontend()
    
    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
                print("✅ Backend stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("🔪 Backend force killed")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("🔪 Frontend force killed")
    
    def run_system_test(self):
        """Run system tests to verify everything is working"""
        print("\n🧪 Running system tests...")
        
        try:
            result = subprocess.run([sys.executable, 'test_system.py'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ System tests passed")
                return True
            else:
                print("❌ System tests failed:")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ System tests timed out")
            return False
        except Exception as e:
            print(f"❌ System test error: {e}")
            return False
    
    def start_system(self):
        """Start the complete system"""
        print("🚀 LOAN PREDICTION SYSTEM STARTUP")
        print("=" * 50)
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            return False
        
        # Step 2: Setup database
        if not self.setup_database():
            print("❌ Database setup failed")
            return False
        
        # Step 3: Start backend
        if not self.start_backend():
            print("❌ Backend startup failed")
            return False
        
        # Step 4: Start frontend
        if not self.start_frontend():
            print("❌ Frontend startup failed")
            self.stop_all()
            return False
        
        # Step 5: Run tests
        time.sleep(5)  # Wait for services to fully start
        test_passed = self.run_system_test()
        
        # Print status
        print("\n" + "=" * 50)
        print("🎉 SYSTEM STARTUP COMPLETE!")
        print("=" * 50)
        print("\n🌐 Access Points:")
        print("   • Frontend:  http://localhost:3000")
        print("   • API:       http://localhost:5000")
        print("   • Health:    http://localhost:5000/api/health")
        
        if test_passed:
            print("\n✅ All system tests passed")
        else:
            print("\n⚠️  Some tests failed, but system is running")
        
        print("\n📋 Available Features:")
        print("   • Loan Prediction with ML models")
        print("   • Real-time Dashboard Analytics")
        print("   • User Authentication (optional)")
        print("   • Database Integration")
        
        print("\n🔧 Controls:")
        print("   • Press Ctrl+C to stop all services")
        print("   • Check logs in terminal for debugging")
        
        # Set up signal handler for graceful shutdown
        def signal_handler(sig, frame):
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()
        
        return True

def main():
    """Main function"""
    manager = SystemManager()
    
    try:
        success = manager.start_system()
        if not success:
            print("\n❌ System startup failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        manager.stop_all()
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        manager.stop_all()
        sys.exit(1)

if __name__ == "__main__":
    main()