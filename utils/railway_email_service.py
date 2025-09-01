"""
Enhanced Email Service for Railway.com Deployment
Handles email notifications with proper error handling and Railway-specific configurations
"""
import os
import logging
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class RailwayEmailService:
    """Enhanced email service for Railway.com deployment"""
    
    @staticmethod
    def test_email_connection():
        """Test email connection and configuration"""
        try:
            from django.core.mail import get_connection
            
            connection = get_connection()
            connection.open()
            connection.close()
            
            logger.info("✅ Email connection test successful")
            return True, "Email connection successful"
            
        except Exception as e:
            logger.error(f"❌ Email connection test failed: {e}")
            return False, str(e)
    
    @staticmethod
    def get_email_config_status():
        """Get current email configuration status"""
        config = {
            'backend': getattr(settings, 'EMAIL_BACKEND', 'Not set'),
            'host': getattr(settings, 'EMAIL_HOST', 'Not set'),
            'port': getattr(settings, 'EMAIL_PORT', 'Not set'),
            'use_tls': getattr(settings, 'EMAIL_USE_TLS', 'Not set'),
            'user': getattr(settings, 'EMAIL_HOST_USER', 'Not set'),
            'password_set': bool(getattr(settings, 'EMAIL_HOST_PASSWORD', None)),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set'),
            'admin_email': getattr(settings, 'ADMIN_EMAIL', 'Not set'),
            'railway_env': os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Not Railway'),
            'is_railway': bool(os.environ.get('RAILWAY')),
        }
        
        logger.info(f"Email configuration: {config}")
        return config
    
    @staticmethod
    def send_notification_with_fallback(subject, message, recipient_list, html_message=None):
        """Send email with multiple fallback methods"""
        
        # Log the attempt
        logger.info(f"🔄 Attempting to send email: {subject}")
        logger.info(f"   Recipients: {recipient_list}")
        logger.info(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        
        # Get email config status
        config = RailwayEmailService.get_email_config_status()
        logger.info(f"   Email config: {config}")
        
        # Method 1: Try Django's send_mail
        try:
            success = send_mail(
                subject=subject,
                message=strip_tags(message) if html_message else message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            
            if success:
                logger.info(f"✅ Email sent successfully via Django send_mail")
                return True, "Email sent successfully"
            else:
                logger.warning(f"⚠️  Django send_mail returned False")
                
        except Exception as e:
            logger.error(f"❌ Django send_mail failed: {e}")
        
        # Method 2: Try EmailMessage
        try:
            email = EmailMessage(
                subject=subject,
                body=html_message or message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list,
            )
            
            if html_message:
                email.content_subtype = 'html'
            
            result = email.send(fail_silently=False)
            
            if result:
                logger.info(f"✅ Email sent successfully via EmailMessage")
                return True, "Email sent via EmailMessage"
            else:
                logger.warning(f"⚠️  EmailMessage send returned False")
                
        except Exception as e:
            logger.error(f"❌ EmailMessage failed: {e}")
        
        # Method 3: Try direct SMTP (for Railway.com)
        if os.environ.get('RAILWAY') and settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            try:
                return RailwayEmailService.send_via_smtp(subject, message, recipient_list, html_message)
            except Exception as e:
                logger.error(f"❌ Direct SMTP failed: {e}")
        
        # All methods failed
        logger.error(f"❌ All email sending methods failed")
        return False, "All email sending methods failed"
    
    @staticmethod
    def send_via_smtp(subject, message, recipient_list, html_message=None):
        """Send email via direct SMTP connection (Railway.com fallback)"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = ', '.join(recipient_list)
            
            # Add text part
            text_part = MIMEText(strip_tags(message) if html_message else message, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_message:
                html_part = MIMEText(html_message, 'html')
                msg.attach(html_part)
            
            # Connect to SMTP server
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            # Send email
            text = msg.as_string()
            server.sendmail(settings.DEFAULT_FROM_EMAIL, recipient_list, text)
            server.quit()
            
            logger.info(f"✅ Email sent successfully via direct SMTP")
            return True, "Email sent via direct SMTP"
            
        except Exception as e:
            logger.error(f"❌ Direct SMTP failed: {e}")
            return False, f"Direct SMTP failed: {e}"
    
    @staticmethod
    def send_test_email(recipient_email=None):
        """Send a test email to verify configuration"""
        recipient = recipient_email or getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
        
        subject = "🧪 PipsMade Email Test - Railway.com"
        message = f"""
        Email Test from PipsMade
        
        This is a test email to verify that email notifications are working correctly on Railway.com.
        
        Configuration Details:
        - Environment: {os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Unknown')}
        - Railway: {bool(os.environ.get('RAILWAY'))}
        - Email Backend: {settings.EMAIL_BACKEND}
        - Email Host: {settings.EMAIL_HOST}
        - Email Port: {settings.EMAIL_PORT}
        - Email User: {settings.EMAIL_HOST_USER}
        - From Email: {settings.DEFAULT_FROM_EMAIL}
        
        If you receive this email, the email system is working correctly!
        
        Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        html_message = f"""
        <html>
        <body>
            <h2>🧪 PipsMade Email Test - Railway.com</h2>
            <p>This is a test email to verify that email notifications are working correctly on Railway.com.</p>
            
            <h3>Configuration Details:</h3>
            <ul>
                <li><strong>Environment:</strong> {os.environ.get('RAILWAY_ENVIRONMENT_NAME', 'Unknown')}</li>
                <li><strong>Railway:</strong> {bool(os.environ.get('RAILWAY'))}</li>
                <li><strong>Email Backend:</strong> {settings.EMAIL_BACKEND}</li>
                <li><strong>Email Host:</strong> {settings.EMAIL_HOST}</li>
                <li><strong>Email Port:</strong> {settings.EMAIL_PORT}</li>
                <li><strong>Email User:</strong> {settings.EMAIL_HOST_USER}</li>
                <li><strong>From Email:</strong> {settings.DEFAULT_FROM_EMAIL}</li>
            </ul>
            
            <p><strong>✅ If you receive this email, the email system is working correctly!</strong></p>
            
            <p><small>Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </body>
        </html>
        """
        
        return RailwayEmailService.send_notification_with_fallback(
            subject=subject,
            message=message,
            recipient_list=[recipient],
            html_message=html_message
        )

# Convenience functions for different notification types
def send_login_notification(user):
    """Send login notification using enhanced service"""
    subject = f"🔐 User Login - {user.username}"
    message = f"""
    User Login Notification
    
    User: {user.get_full_name() or user.username}
    Email: {user.email}
    Username: {user.username}
    Time: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'N/A'}
    
    This is an automated notification from PipsMade.
    """
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
    return RailwayEmailService.send_notification_with_fallback(
        subject=subject,
        message=message,
        recipient_list=[admin_email]
    )

def send_signup_notification(user):
    """Send signup notification using enhanced service"""
    subject = f"👤 New User Registration - {user.username}"
    message = f"""
    New User Registration
    
    User: {user.get_full_name() or user.username}
    Email: {user.email}
    Username: {user.username}
    Registration Date: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}
    
    This is an automated notification from PipsMade.
    """
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
    return RailwayEmailService.send_notification_with_fallback(
        subject=subject,
        message=message,
        recipient_list=[admin_email]
    )

def send_deposit_notification(deposit_request):
    """Send deposit notification using enhanced service"""
    subject = f"💰 New Deposit Request - {deposit_request.user.username}"
    message = f"""
    New Deposit Request
    
    User: {deposit_request.user.get_full_name() or deposit_request.user.username}
    Email: {deposit_request.user.email}
    Amount: {deposit_request.amount} {deposit_request.crypto_wallet.crypto_type}
    Transaction Hash: {deposit_request.transaction_hash}
    Network: {deposit_request.crypto_wallet.network}
    Request Date: {deposit_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    This is an automated notification from PipsMade.
    """
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
    return RailwayEmailService.send_notification_with_fallback(
        subject=subject,
        message=message,
        recipient_list=[admin_email]
    )

def send_withdrawal_notification(withdrawal_request):
    """Send withdrawal notification using enhanced service"""
    subject = f"💸 New Withdrawal Request - {withdrawal_request.user.username}"
    message = f"""
    New Withdrawal Request
    
    User: {withdrawal_request.user.get_full_name() or withdrawal_request.user.username}
    Email: {withdrawal_request.user.email}
    Amount: {withdrawal_request.amount} {withdrawal_request.crypto_type}
    Destination: {withdrawal_request.destination_address}
    Network: {withdrawal_request.network}
    Request Date: {withdrawal_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    This is an automated notification from PipsMade.
    """
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
    return RailwayEmailService.send_notification_with_fallback(
        subject=subject,
        message=message,
        recipient_list=[admin_email]
    )
