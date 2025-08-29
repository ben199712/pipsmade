"""
Simple email notification system for accounts
"""
from django.core.mail import send_mail
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

def send_login_notification(user):
    """Send notification when user logs in"""
    try:
        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"Railway environment detected for login notification")
        
        subject = f"User Login Notification - {user.username}"
        
        message = f"""
        User Login Notification
        
        User: {user.get_full_name() or user.username}
        Email: {user.email}
        Username: {user.username}
        Time: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'N/A'}
        
        This is an automated notification from the pipsmade investment platform.
        """
        
        # Send to admin email from settings
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
        
        # Log the attempt
        logger.info(f"Attempting to send login notification to {admin_email}")
        logger.info(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        
        success = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        
        if success:
            logger.info(f"Login notification sent successfully to {admin_email}")
        else:
            logger.error(f"Failed to send login notification to {admin_email}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending login notification: {e}")
        logger.error(f"Email configuration: BACKEND={getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
        logger.error(f"Email host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        logger.error(f"Email user: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
        return False

def send_signup_notification(user):
    """Send notification when new user registers"""
    try:
        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"Railway environment detected for signup notification")
        
        subject = f"New User Registration - {user.username}"
        
        message = f"""
        New User Registration
        
        User: {user.get_full_name() or user.username}
        Email: {user.email}
        Username: {user.username}
        Registration Date: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated notification from the pipsmade investment platform.
        """
        
        # Send to admin email from settings
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')
        
        # Log the attempt
        logger.info(f"Attempting to send signup notification to {admin_email}")
        logger.info(f"Email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        
        success = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        
        if success:
            logger.info(f"Signup notification sent successfully to {admin_email}")
        else:
            logger.error(f"Failed to send signup notification to {admin_email}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending signup notification: {e}")
        logger.error(f"Email configuration: BACKEND={getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
        logger.error(f"Email host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        logger.error(f"Email user: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
        return False 