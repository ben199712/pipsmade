#!/usr/bin/env python
"""
Test email functionality after domain configuration on Railway.com
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from utils.railway_email_service import RailwayEmailService

def main():
    print("🌐 Railway.com Domain Email Test")
    print("=" * 50)
    
    # Environment detection
    print(f"\n🔍 Environment Detection:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   RAILWAY env var: {os.environ.get('RAILWAY', 'Not set')}")
    print(f"   RAILWAY_ENVIRONMENT_NAME: {os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Not set')}")
    print(f"   RAILWAY_PUBLIC_DOMAIN: {os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'Not set')}")
    print(f"   CUSTOM_DOMAIN: {os.environ.get('CUSTOM_DOMAIN', 'Not set')}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Email configuration check
    print(f"\n📧 Email Configuration:")
    print(f"   Backend: {settings.EMAIL_BACKEND}")
    print(f"   Host: {settings.EMAIL_HOST}")
    print(f"   Port: {settings.EMAIL_PORT}")
    print(f"   Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"   Host User: {settings.EMAIL_HOST_USER}")
    print(f"   Password Set: {'✅ Yes' if settings.EMAIL_HOST_PASSWORD else '❌ No'}")
    print(f"   From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   Admin Email: {settings.ADMIN_EMAIL}")
    
    # Check if using SMTP backend
    if 'console' in settings.EMAIL_BACKEND.lower():
        print(f"\n⚠️  WARNING: Using console email backend!")
        print(f"   This means emails will only show in logs, not actually send")
        print(f"   Check your environment variables and Railway settings")
        return
    
    # Test email connection
    print(f"\n🔌 Testing Email Connection:")
    try:
        success, message = RailwayEmailService.test_email_connection()
        if success:
            print(f"   ✅ Connection successful: {message}")
        else:
            print(f"   ❌ Connection failed: {message}")
            show_domain_troubleshooting()
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        show_domain_troubleshooting()
        return
    
    # Send test email
    print(f"\n📤 Sending Test Email:")
    admin_email = settings.ADMIN_EMAIL
    print(f"   To: {admin_email}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        # Test with enhanced service
        success, message = RailwayEmailService.send_test_email(admin_email)
        
        if success:
            print(f"   ✅ Enhanced service test: {message}")
        else:
            print(f"   ❌ Enhanced service failed: {message}")
        
        # Test with basic Django send_mail
        print(f"\n📧 Testing Basic Django send_mail:")
        basic_success = send_mail(
            subject='🧪 Railway Domain Email Test',
            message=f'''
            Domain Email Test from Railway.com
            
            This email confirms that your email system is working after domain configuration.
            
            Environment Details:
            - Railway Domain: {os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'Not set')}
            - Custom Domain: {os.environ.get('CUSTOM_DOMAIN', 'Not set')}
            - Email Backend: {settings.EMAIL_BACKEND}
            - From Email: {settings.DEFAULT_FROM_EMAIL}
            
            If you receive this email, your domain email configuration is working!
            
            Time: {__import__('datetime').datetime.now()}
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        
        if basic_success:
            print(f"   ✅ Basic Django send_mail successful")
            print(f"   📬 Check your inbox at: {admin_email}")
        else:
            print(f"   ❌ Basic Django send_mail failed")
            
    except Exception as e:
        print(f"   ❌ Email test error: {e}")
        show_domain_troubleshooting()
    
    print(f"\n🎉 Domain email test completed!")

def show_domain_troubleshooting():
    print(f"\n🔧 Domain-Specific Troubleshooting:")
    
    print(f"\n1️⃣ Railway Environment Variables:")
    print(f"   Go to Railway Dashboard > Your Project > Variables")
    print(f"   Ensure these are set:")
    print(f"   • EMAIL_HOST_USER=Celewizzy106@gmail.com")
    print(f"   • EMAIL_HOST_PASSWORD=your-app-password")
    print(f"   • ADMIN_EMAIL=Celewizzy106@gmail.com")
    print(f"   • DEFAULT_FROM_EMAIL=support@pipsmade.com")
    print(f"   • CUSTOM_DOMAIN=your-domain.com (if using custom domain)")
    
    print(f"\n2️⃣ Domain Configuration:")
    print(f"   • Ensure your domain is properly connected in Railway")
    print(f"   • Check DNS settings are correct")
    print(f"   • Verify SSL certificate is active")
    
    print(f"\n3️⃣ Gmail Settings:")
    print(f"   • Ensure 2FA is enabled on Gmail account")
    print(f"   • Use App Password, not regular password")
    print(f"   • Check if Gmail is blocking Railway IP addresses")
    
    print(f"\n4️⃣ Railway Logs:")
    print(f"   • Run: railway logs --tail")
    print(f"   • Look for email-related errors")
    print(f"   • Check for SMTP connection issues")
    
    print(f"\n5️⃣ Alternative Email Services:")
    print(f"   Consider using SendGrid, Mailgun, or AWS SES")
    print(f"   These are more reliable for production hosting")

def test_specific_notification():
    """Test a specific notification type"""
    print(f"\n🧪 Testing Specific Notifications:")
    
    try:
        from django.contrib.auth.models import User
        
        # Get or create a test user
        test_user, created = User.objects.get_or_create(
            username='test_email_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Test login notification
        from accounts.email_notifications import send_login_notification
        login_success = send_login_notification(test_user)
        print(f"   Login notification: {'✅ Success' if login_success else '❌ Failed'}")
        
        # Test signup notification  
        from accounts.email_notifications import send_signup_notification
        signup_success = send_signup_notification(test_user)
        print(f"   Signup notification: {'✅ Success' if signup_success else '❌ Failed'}")
        
        # Clean up test user if created
        if created:
            test_user.delete()
            
    except Exception as e:
        print(f"   ❌ Notification test error: {e}")

if __name__ == '__main__':
    main()
    
    # Also test specific notifications
    test_specific_notification()
