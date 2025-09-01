#!/usr/bin/env python
"""
Quick test script for Railway.com email functionality
Run this on Railway to test email system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.conf import settings
from utils.railway_email_service import RailwayEmailService

def main():
    print("🧪 Railway.com Email Test Script")
    print("=" * 50)
    
    # Check environment
    print(f"\n🌍 Environment Check:")
    print(f"   Railway Environment: {os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Not Railway')}")
    print(f"   Railway Detected: {bool(os.environ.get('RAILWAY'))}")
    print(f"   Debug Mode: {settings.DEBUG}")
    
    # Check email configuration
    print(f"\n📧 Email Configuration:")
    config = RailwayEmailService.get_email_config_status()
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Test connection
    print(f"\n🔌 Testing Email Connection:")
    try:
        success, message = RailwayEmailService.test_email_connection()
        if success:
            print(f"   ✅ Connection successful: {message}")
        else:
            print(f"   ❌ Connection failed: {message}")
            show_troubleshooting()
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        show_troubleshooting()
        return
    
    # Send test email
    print(f"\n📤 Sending Test Email:")
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
    print(f"   Recipient: {admin_email}")
    
    try:
        success, message = RailwayEmailService.send_test_email(admin_email)
        if success:
            print(f"   ✅ Test email sent: {message}")
            print(f"   📬 Check your inbox at: {admin_email}")
        else:
            print(f"   ❌ Test email failed: {message}")
            show_troubleshooting()
    except Exception as e:
        print(f"   ❌ Test email error: {e}")
        show_troubleshooting()
    
    print(f"\n🎉 Email test completed!")

def show_troubleshooting():
    print(f"\n🔧 Troubleshooting Tips:")
    print(f"   1. Check Gmail App Password is set correctly")
    print(f"   2. Verify Railway environment variables:")
    print(f"      - EMAIL_HOST_USER")
    print(f"      - EMAIL_HOST_PASSWORD") 
    print(f"      - ADMIN_EMAIL")
    print(f"   3. Check Railway logs: railway logs")
    print(f"   4. See RAILWAY_EMAIL_SETUP.md for detailed guide")

if __name__ == '__main__':
    main()
