"""
Management command to test email functionality on Railway.com
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Test email functionality for Railway.com deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to (defaults to ADMIN_EMAIL)',
        )
        parser.add_argument(
            '--config',
            action='store_true',
            help='Show email configuration details',
        )
        parser.add_argument(
            '--test-connection',
            action='store_true',
            help='Test email connection only',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testing Email System for Railway.com'))
        
        # Show environment info
        self.stdout.write(f"\n🌍 Environment Information:")
        self.stdout.write(f"   Railway Environment: {os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Not Railway')}")
        self.stdout.write(f"   Railway Detected: {bool(os.environ.get('RAILWAY'))}")
        self.stdout.write(f"   Debug Mode: {settings.DEBUG}")
        
        # Show email configuration
        if options['config'] or options['test_connection']:
            self.show_email_config()
        
        # Test connection
        if options['test_connection']:
            self.test_connection()
            return
        
        # Send test email
        recipient_email = options['email'] or getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
        self.send_test_email(recipient_email)

    def show_email_config(self):
        """Show current email configuration"""
        self.stdout.write(f"\n📧 Email Configuration:")
        
        config_items = [
            ('Backend', getattr(settings, 'EMAIL_BACKEND', 'Not set')),
            ('Host', getattr(settings, 'EMAIL_HOST', 'Not set')),
            ('Port', getattr(settings, 'EMAIL_PORT', 'Not set')),
            ('Use TLS', getattr(settings, 'EMAIL_USE_TLS', 'Not set')),
            ('Use SSL', getattr(settings, 'EMAIL_USE_SSL', 'Not set')),
            ('Host User', getattr(settings, 'EMAIL_HOST_USER', 'Not set')),
            ('Password Set', '✅ Yes' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else '❌ No'),
            ('From Email', getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')),
            ('Admin Email', getattr(settings, 'ADMIN_EMAIL', 'Not set')),
            ('Timeout', getattr(settings, 'EMAIL_TIMEOUT', 'Not set')),
        ]
        
        for key, value in config_items:
            self.stdout.write(f"   {key}: {value}")
        
        # Check environment variables
        self.stdout.write(f"\n🔧 Environment Variables:")
        env_vars = [
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'DEFAULT_FROM_EMAIL',
            'ADMIN_EMAIL',
            'RAILWAY_ENVIRONMENT_NAME',
            'RAILWAY'
        ]
        
        for var in env_vars:
            value = os.environ.get(var)
            if var == 'EMAIL_HOST_PASSWORD' and value:
                value = '***' + value[-4:] if len(value) > 4 else '***'
            status = '✅ Set' if value else '❌ Not set'
            self.stdout.write(f"   {var}: {status} ({value if value and var != 'EMAIL_HOST_PASSWORD' else ''})")

    def test_connection(self):
        """Test email connection"""
        self.stdout.write(f"\n🔌 Testing Email Connection:")
        
        try:
            from utils.railway_email_service import RailwayEmailService
            
            success, message = RailwayEmailService.test_email_connection()
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"   ✅ Connection successful: {message}"))
            else:
                self.stdout.write(self.style.ERROR(f"   ❌ Connection failed: {message}"))
                
                # Show troubleshooting tips
                self.show_troubleshooting_tips()
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Connection test error: {e}"))
            self.show_troubleshooting_tips()

    def send_test_email(self, recipient_email):
        """Send a test email"""
        self.stdout.write(f"\n📤 Sending Test Email to: {recipient_email}")
        
        try:
            from utils.railway_email_service import RailwayEmailService
            
            success, message = RailwayEmailService.send_test_email(recipient_email)
            
            if success:
                self.stdout.write(self.style.SUCCESS(f"   ✅ Test email sent successfully: {message}"))
                self.stdout.write(f"   📬 Check your inbox at: {recipient_email}")
            else:
                self.stdout.write(self.style.ERROR(f"   ❌ Test email failed: {message}"))
                self.show_troubleshooting_tips()
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Test email error: {e}"))
            self.show_troubleshooting_tips()

    def show_troubleshooting_tips(self):
        """Show troubleshooting tips for Railway.com"""
        self.stdout.write(f"\n🔧 Troubleshooting Tips for Railway.com:")
        
        self.stdout.write(f"\n1️⃣ Check Gmail App Password:")
        self.stdout.write(f"   • Go to Google Account settings")
        self.stdout.write(f"   • Enable 2-Factor Authentication")
        self.stdout.write(f"   • Generate App Password for 'Mail'")
        self.stdout.write(f"   • Use App Password (not regular password)")
        
        self.stdout.write(f"\n2️⃣ Set Railway Environment Variables:")
        self.stdout.write(f"   • Go to Railway Dashboard > Your Project > Variables")
        self.stdout.write(f"   • Add: EMAIL_HOST_USER = your-email@gmail.com")
        self.stdout.write(f"   • Add: EMAIL_HOST_PASSWORD = your-app-password")
        self.stdout.write(f"   • Add: ADMIN_EMAIL = your-admin@email.com")
        self.stdout.write(f"   • Add: DEFAULT_FROM_EMAIL = your-email@gmail.com")
        
        self.stdout.write(f"\n3️⃣ Alternative Email Services:")
        self.stdout.write(f"   • Consider using SendGrid, Mailgun, or AWS SES")
        self.stdout.write(f"   • These services are more reliable for production")
        self.stdout.write(f"   • Gmail SMTP can be blocked by some hosting providers")
        
        self.stdout.write(f"\n4️⃣ Check Railway Logs:")
        self.stdout.write(f"   • Run: railway logs")
        self.stdout.write(f"   • Look for email-related errors")
        self.stdout.write(f"   • Check for connection timeouts")
        
        self.stdout.write(f"\n5️⃣ Test Locally First:")
        self.stdout.write(f"   • Test email on local development")
        self.stdout.write(f"   • Ensure credentials work outside Railway")
        self.stdout.write(f"   • Use same settings locally and on Railway")

    def handle_error(self, error_message):
        """Handle and display errors"""
        self.stdout.write(self.style.ERROR(f"❌ Error: {error_message}"))
        self.show_troubleshooting_tips()
