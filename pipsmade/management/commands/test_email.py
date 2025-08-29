from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Test email functionality on Railway deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to',
            default='admin@pipsmade.com'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write(
            self.style.SUCCESS('Testing email functionality...')
        )
        
        # Display current email configuration
        self.stdout.write(f"Email Backend: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
        self.stdout.write(f"Email Host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        self.stdout.write(f"Email Port: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
        self.stdout.write(f"Email User: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
        self.stdout.write(f"Email TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
        self.stdout.write(f"Default From: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
        self.stdout.write(f"Admin Email: {getattr(settings, 'ADMIN_EMAIL', 'Not set')}")
        
        # Check environment
        if os.environ.get('RAILWAY'):
            self.stdout.write(
                self.style.SUCCESS('✓ Railway environment detected')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Not in Railway environment')
            )
        
        # Test email sending
        try:
            subject = "Test Email from PipsMade Railway Deployment"
            message = f"""
            This is a test email from your PipsMade application deployed on Railway.
            
            Environment: {'Railway' if os.environ.get('RAILWAY') else 'Local/Other'}
            Email Backend: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}
            Email Host: {getattr(settings, 'EMAIL_HOST', 'Not set')}
            
            If you receive this email, your email configuration is working correctly!
            """
            
            self.stdout.write(f"Sending test email to: {test_email}")
            
            success = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✓ Test email sent successfully!')
                )
                self.stdout.write(
                    self.style.SUCCESS('Your email notifications should now work on Railway.')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('✗ Failed to send test email')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error sending test email: {e}')
            )
            self.stdout.write(
                self.style.WARNING('Check your email configuration and Railway environment variables.')
            )
