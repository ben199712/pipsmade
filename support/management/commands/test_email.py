from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = 'Test email functionality for support system'

    def handle(self, *args, **options):
        self.stdout.write('Testing email functionality...')
        
        try:
            # Test basic email sending
            send_mail(
                subject='Test Email from PipsMade Support System',
                message=f'''
                This is a test email from the PipsMade support system.
                
                Sent at: {timezone.now()}
                Email backend: {settings.EMAIL_BACKEND}
                
                If you receive this email, the email system is working correctly!
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Test email sent successfully to {settings.ADMIN_EMAIL}'
                )
            )
            
            # Show current email configuration
            self.stdout.write('\n📧 Current Email Configuration:')
            self.stdout.write(f'   Backend: {settings.EMAIL_BACKEND}')
            self.stdout.write(f'   From Email: {settings.DEFAULT_FROM_EMAIL}')
            self.stdout.write(f'   Admin Email: {settings.ADMIN_EMAIL}')
            self.stdout.write(f'   Support Email: {getattr(settings, "SUPPORT_EMAIL", "Not set")}')
            
            if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
                self.stdout.write(
                    self.style.WARNING(
                        '⚠️  Using console backend - emails will be printed to console only'
                    )
                )
                self.stdout.write(
                    '   To enable real email sending, update EMAIL_BACKEND in settings.py'
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send test email: {str(e)}')
            )
            self.stdout.write('   Check your email configuration in settings.py') 