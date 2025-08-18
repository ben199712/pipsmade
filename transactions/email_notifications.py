"""
Simple email notification system for transactions
"""
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_deposit_notification(deposit_request):
    """Send notification when user makes deposit request"""
    try:
        subject = f"New Deposit Request - {deposit_request.user.username}"
        
        message = f"""
        New Deposit Request
        
        User: {deposit_request.user.get_full_name() or deposit_request.user.username}
        Email: {deposit_request.user.email}
        Amount: {deposit_request.amount} {deposit_request.crypto_wallet.crypto_type}
        Transaction Hash: {deposit_request.transaction_hash}
        Sender Address: {deposit_request.sender_address}
        Network: {deposit_request.crypto_wallet.network}
        Request Date: {deposit_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        View in admin: /admin/transactions/depositrequest/{deposit_request.id}/
        
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
            logger.info(f"Deposit notification sent successfully to {admin_email}")
        else:
            logger.error(f"Failed to send deposit notification to {admin_email}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending deposit notification: {e}")
        return False

def send_withdrawal_notification(withdrawal_request):
    """Send notification when user makes withdrawal request"""
    try:
        subject = f"New Withdrawal Request - {withdrawal_request.user.username}"
        
        message = f"""
        New Withdrawal Request
        
        User: {withdrawal_request.user.get_full_name() or withdrawal_request.user.username}
        Email: {withdrawal_request.user.email}
        Amount: {withdrawal_request.amount} {withdrawal_request.crypto_type}
        Destination Address: {withdrawal_request.destination_address}
        Network: {withdrawal_request.network}
        Network Fee: {withdrawal_request.network_fee}
        Platform Fee: {withdrawal_request.platform_fee}
        Net Amount: {withdrawal_request.net_amount()}
        Request Date: {withdrawal_request.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        View in admin: /admin/transactions/withdrawalrequest/{withdrawal_request.id}/
        
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
            logger.info(f"Withdrawal notification sent successfully to {admin_email}")
        else:
            logger.error(f"Failed to send withdrawal notification to {admin_email}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending withdrawal notification: {e}")
        return False 