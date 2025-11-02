#!/usr/bin/env python3
"""
Email Setup Helper for Contact Form
Helps you configure EmailJS for real email sending
"""

import os
import webbrowser
from pathlib import Path

def print_header():
    print("📧 EMAIL SETUP HELPER FOR CONTACT FORM")
    print("=" * 50)
    print("This will help you set up real email sending for your contact form.")
    print("We'll use EmailJS - it's free, easy, and works great with React!\n")

def open_emailjs():
    print("🚀 Step 1: Create EmailJS Account")
    print("-" * 30)
    print("I'll open EmailJS website for you...")
    
    try:
        webbrowser.open("https://www.emailjs.com/")
        print("✅ EmailJS website opened in your browser")
        print("\n📋 What to do:")
        print("   1. Click 'Sign Up' and create a free account")
        print("   2. Verify your email address")
        print("   3. Come back here when done")
        
        input("\n⏳ Press Enter when you've created your EmailJS account...")
        return True
    except:
        print("❌ Couldn't open browser automatically")
        print("🌐 Please go to: https://www.emailjs.com/")
        return False

def setup_service():
    print("\n🔧 Step 2: Add Email Service")
    print("-" * 30)
    print("📋 In your EmailJS dashboard:")
    print("   1. Go to 'Email Services'")
    print("   2. Click 'Add New Service'")
    print("   3. Choose 'Gmail' (recommended)")
    print("   4. Click 'Connect Account'")
    print("   5. Sign in with: aman.devrani6921@gmail.com")
    print("   6. Allow all permissions")
    print("   7. Copy the SERVICE ID (looks like: service_xxxxxxx)")
    
    service_id = input("\n📝 Enter your SERVICE ID: ").strip()
    return service_id

def setup_template():
    print("\n📝 Step 3: Create Email Template")
    print("-" * 30)
    print("📋 In your EmailJS dashboard:")
    print("   1. Go to 'Email Templates'")
    print("   2. Click 'Create New Template'")
    print("   3. Set Subject: 'New Contact Form Message - {{subject}}'")
    print("   4. Copy this template content:")
    
    template_content = """
From: {{from_name}} ({{from_email}})
Subject: {{subject}}
Timestamp: {{timestamp}}

Message:
{{message}}

---
This message was sent from your LoanPredict AI contact form.
Reply directly to {{reply_to}} to respond to the sender.
"""
    
    print("\n" + "="*50)
    print("TEMPLATE CONTENT (copy this):")
    print("="*50)
    print(template_content)
    print("="*50)
    
    print("\n   5. Save the template")
    print("   6. Copy the TEMPLATE ID (looks like: template_xxxxxxx)")
    
    template_id = input("\n📝 Enter your TEMPLATE ID: ").strip()
    return template_id

def get_public_key():
    print("\n🔑 Step 4: Get Public Key")
    print("-" * 30)
    print("📋 In your EmailJS dashboard:")
    print("   1. Go to 'Account' → 'General'")
    print("   2. Copy your Public Key (looks like: xxxxxxxxxx)")
    
    public_key = input("\n📝 Enter your PUBLIC KEY: ").strip()
    return public_key

def update_config_file(service_id, template_id, public_key):
    print("\n💾 Step 5: Updating Configuration")
    print("-" * 30)
    
    config_path = Path("src/config/email.js")
    
    if not config_path.exists():
        print("❌ Config file not found. Make sure you're in the project directory.")
        return False
    
    try:
        # Read current config
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Replace the placeholder values
        content = content.replace('service_your_id', service_id)
        content = content.replace('template_your_id', template_id)
        content = content.replace('your_public_key', public_key)
        
        # Write updated config
        with open(config_path, 'w') as f:
            f.write(content)
        
        print("✅ Configuration file updated successfully!")
        print(f"📁 Updated: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        return False

def test_setup():
    print("\n🧪 Step 6: Test Your Setup")
    print("-" * 30)
    print("📋 To test your email setup:")
    print("   1. Start your React app: npm start")
    print("   2. Go to the Contact page")
    print("   3. Fill out and submit the form")
    print("   4. Check aman.devrani6921@gmail.com for the email")
    print("   5. Check browser console for any errors")
    
    print("\n🔧 Troubleshooting:")
    print("   • If no email arrives, check spam folder")
    print("   • Verify all IDs are correct in src/config/email.js")
    print("   • Make sure EmailJS service is connected")
    print("   • Check browser console for error messages")

def main():
    print_header()
    
    # Check if we're in the right directory
    if not Path("src/config/email.js").exists():
        print("❌ Error: Not in the correct project directory")
        print("💡 Navigate to your project folder and run this script again")
        return
    
    try:
        # Step 1: Open EmailJS
        if not open_emailjs():
            print("Please create your EmailJS account manually and come back")
            return
        
        # Step 2: Setup service
        service_id = setup_service()
        if not service_id:
            print("❌ Service ID is required")
            return
        
        # Step 3: Setup template
        template_id = setup_template()
        if not template_id:
            print("❌ Template ID is required")
            return
        
        # Step 4: Get public key
        public_key = get_public_key()
        if not public_key:
            print("❌ Public key is required")
            return
        
        # Step 5: Update config
        if update_config_file(service_id, template_id, public_key):
            print("\n🎉 EMAIL SETUP COMPLETE!")
            print("=" * 50)
            print("✅ EmailJS account created")
            print("✅ Gmail service connected")
            print("✅ Email template created")
            print("✅ Configuration file updated")
            
            print(f"\n📧 Emails will be sent to: aman.devrani6921@gmail.com")
            print("🌐 Your contact form is now ready to send real emails!")
            
            test_setup()
        else:
            print("❌ Setup failed. Please check the errors above.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. Run this script again when ready!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()