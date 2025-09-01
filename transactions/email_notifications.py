"""
Enhanced email notification system for transactions - Railway.com compatible
"""
import logging
import os

logger = logging.getLogger(__name__)

def send_deposit_notification(deposit_request):
    """Send notification when user makes deposit request"""
    try:
        # Use enhanced Railway email service
        from utils.railway_email_service import send_deposit_notification as enhanced_send_deposit

        logger.info(f"🔄 Sending deposit notification for user: {deposit_request.user.username}")

        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"🚂 Railway environment detected for deposit notification")

        success, message = enhanced_send_deposit(deposit_request)

        if success:
            logger.info(f"✅ Deposit notification sent successfully: {message}")
        else:
            logger.error(f"❌ Failed to send deposit notification: {message}")

        return success

    except Exception as e:
        logger.error(f"❌ Error in deposit notification system: {e}")

        # Fallback to basic logging
        logger.info(f"📝 DEPOSIT EVENT: User {deposit_request.user.username} deposited {deposit_request.amount} {deposit_request.crypto_wallet.crypto_type}")
        return False

def send_withdrawal_notification(withdrawal_request):
    """Send notification when user makes withdrawal request"""
    try:
        # Use enhanced Railway email service
        from utils.railway_email_service import send_withdrawal_notification as enhanced_send_withdrawal

        logger.info(f"🔄 Sending withdrawal notification for user: {withdrawal_request.user.username}")

        # Check if we're in Railway production environment
        if os.environ.get('RAILWAY'):
            logger.info(f"🚂 Railway environment detected for withdrawal notification")

        success, message = enhanced_send_withdrawal(withdrawal_request)

        if success:
            logger.info(f"✅ Withdrawal notification sent successfully: {message}")
        else:
            logger.error(f"❌ Failed to send withdrawal notification: {message}")

        return success

    except Exception as e:
        logger.error(f"❌ Error in withdrawal notification system: {e}")

        # Fallback to basic logging
        logger.info(f"📝 WITHDRAWAL EVENT: User {withdrawal_request.user.username} requested withdrawal of {withdrawal_request.amount} {withdrawal_request.crypto_type}")
        return False