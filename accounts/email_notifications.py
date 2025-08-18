"""
Simple email notification system for accounts
"""
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_login_notification(user):
    """Send notification when user logs in"""
    try:
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
        return False

def send_signup_notification(user):
    """Send notification when new user registers"""
    try:
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
        return False 