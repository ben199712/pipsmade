"""
Enhanced email notification system for accounts - Railway.com compatible
"""
import logging
import os

logger = logging.getLogger(__name__)

def send_login_notification(user):
    """Send notification when user logs in"""
    try:
        # Use enhanced Railway email service
        from utils.railway_email_service import send_login_notification as enhanced_send_login

        logger.info(f"🔄 Sending login notification for user: {user.username}")

        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"🚂 Railway environment detected for login notification")

        success, message = enhanced_send_login(user)

        if success:
            logger.info(f"✅ Login notification sent successfully: {message}")
        else:
            logger.error(f"❌ Failed to send login notification: {message}")

        return success

    except Exception as e:
        logger.error(f"❌ Error in login notification system: {e}")

        # Fallback to basic logging
        logger.info(f"📝 LOGIN EVENT: User {user.username} ({user.email}) logged in at {user.last_login}")
        return False

def send_signup_notification(user):
    """Send notification when new user registers"""
    try:
        # Use enhanced Railway email service
        from utils.railway_email_service import send_signup_notification as enhanced_send_signup

        logger.info(f"🔄 Sending signup notification for user: {user.username}")

        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"🚂 Railway environment detected for signup notification")

        success, message = enhanced_send_signup(user)

        if success:
            logger.info(f"✅ Signup notification sent successfully: {message}")
        else:
            logger.error(f"❌ Failed to send signup notification: {message}")

        return success

    except Exception as e:
        logger.error(f"❌ Error in signup notification system: {e}")

        # Fallback to basic logging
        logger.info(f"📝 SIGNUP EVENT: New user {user.username} ({user.email}) registered at {user.date_joined}")
        return False