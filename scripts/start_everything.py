#!/usr/bin/env python3
"""
Complete System Launcher - Starts everything with one command
Includes email setup, backend, frontend, and system checks
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("🚀 LOANPREDICT AI - COMPLETE SYSTEM LAUNCHER")
    print("=" * 60)
    print("This will start your complete loan prediction system")
    print("Including: Backend API + Frontend + Email Setup")
    print("=" * 60)

def quick_email_setup():
    """Super quick email setup - just get the essentials"""
    config_path = Path("src/config/email.js")
    
    if not config_path.exists():
        print("❌ Email config file missing")
        return False
    
    # Check if already configured
    with open(config_path, 'r') as f:
        content = f.read()
    
    if 'service_your_id' not in content:
        print("✅ Email already configured")
        return True
    
    print("\n📧 QUICK EMAIL SETUP")
    print("-" * 30)
    print("Want to enable real email sending from contact form?")
    print("📧 Emails will be sent to: aman.devrani6921@gmail.com")
    
    response = input("\n❓ Enable real emails? (y/n): ").lower().strip()
    
    if response != 'y':
        print("⏭️  Skipping - contact form will work in demo mode")
        return True
    
    print("\n🔧 Setting up EmailJS (takes 2 minutes)...")
    print("\n📋 Quick Steps:")
    print("   1. I'll open EmailJS.com")
    print("   2. Sign up (free)")
    print("   3. Add Gmail service")
    print("   4. Create template")
    print("   5. Give me 3 IDs")
    
    input("\n⏳ Press Enter to open EmailJS...")
    
    try:
        webbrowser.open("https://www.emailjs.com/")
        print("✅ EmailJS opened in browser")
    except:
        print("🌐 Go to: https://www.emailjs.com/")
    
    print("\n" + "="*50)
    print("EMAIL TEMPLATE (copy this to EmailJS):")
    print("="*50)
    print("Subject: Contact Form - {{subject}}")
    print("")
    print("From: {{from_name}} ({{from_email}})")
    print("Subject: {{subject}}")
    print("Time: {{timestamp}}")
    print("")
    print("{{message}}")
    print("")
    print("---")
    print("Reply to: {{reply_to}}")
    print("="*50)
    
    print("\n📝 After setup, enter your IDs:")
    service_id = input("Service ID: ").strip()
    template_id = input("Template ID: ").strip()
    public_key = input("Public Key: ").strip()
    
    if service_id and template_id and public_key:
        # Update config
        content = content.replace('service_your_id', service_id)
        content = content.replace('template_your_id', template_id)
        content = content.replace('your_public_key', public_key)
        
        with open(config_path, 'w') as f:
            f.write(content)
        
        print("✅ Email configured! Contact form will send real emails.")
        return True
    else:
        print("⏭️  Skipping email setup")
        return True

def start_system():
    """Start the complete system"""
    print("\n🔄 Starting System Components...")
    
    # 1. Quick email check
    quick_email_setup()
    
    # 2. Start backend
    print("\n🚀 Starting Backend API...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, 'backend/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("✅ Backend running on http://localhost:5000")
        else:
            print("❌ Backend failed to start")
            return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False
    
    # 3. Start frontend
    print("\n🌐 Starting Frontend...")
    try:
        frontend_process = subprocess.Popen(
            ['npm', 'start'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Frontend starting... (will open in browser)")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False
    
    # 4. Success message
    print("\n" + "="*60)
    print("🎉 SYSTEM STARTED SUCCESSFULLY!")
    print("="*60)
    print("\n🌐 Your Application:")
    print("   • Frontend:  http://localhost:3000")
    print("   • API:       http://localhost:5000")
    print("   • Contact:   http://localhost:3000/contact")
    
    print("\n📧 Email Status:")
    config_path = Path("src/config/email.js")
    if config_path.exists():
        with open(config_path, 'r') as f:
            content = f.read()
        if 'service_your_id' not in content:
            print("   ✅ Real emails enabled → aman.devrani6921@gmail.com")
        else:
            print("   ⚠️  Demo mode (no real emails)")
    
    print("\n🎯 Test Your System:")
    print("   1. Go to http://localhost:3000")
    print("   2. Try the loan prediction")
    print("   3. Check the dashboard")
    print("   4. Test contact form")
    
    print("\n🔧 Controls:")
    print("   • Press Ctrl+C to stop")
    print("   • System will run until you stop it")
    
    # Keep running
    try:
        print("\n⏳ System running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ System stopped")
    
    return True

def main():
    """Main function"""
    print_banner()
    
    # Check if in right directory
    if not Path("backend/app.py").exists():
        print("❌ Not in project directory")
        print("💡 Navigate to your project folder first")
        return
    
    try:
        start_system()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Error: {e}")

if __name__ == "__main__":
    main()