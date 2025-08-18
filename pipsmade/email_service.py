"""
Email notification service for pipsmade
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .models import AdminEmailConfig
import logging

logger = logging.getLogger(__name__)

class EmailNotificationService:
    """Service for sending email notifications"""
    
    @staticmethod
    def get_admin_emails(notification_type):
        """Get list of admin emails for a specific notification type"""
        try:
            configs = AdminEmailConfig.objects.filter(
                admin_user__is_staff=True,
                **{f'notify_{notification_type}': True}
            )
            emails = []
            for config in configs:
                emails.extend(config.get_notification_emails(notification_type))
            return list(set(emails))  # Remove duplicates
        except Exception as e:
            logger.error(f"Error getting admin emails for {notification_type}: {e}")
            # Fallback to settings
            return [getattr(settings, 'ADMIN_EMAIL', 'admin@pipsmade.com')]
    
    @staticmethod
    def send_notification(subject, message, notification_type, recipient_list=None, html_message=None):
        """Send email notification"""
        try:
            if not recipient_list:
                recipient_list = EmailNotificationService.get_admin_emails(notification_type)
            
            if not recipient_list:
                logger.warning(f"No recipients found for {notification_type} notification")
                return False
            
            # Send email
            success = send_mail(
                subject=subject,
                message=strip_tags(message) if html_message else message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            
            if success:
                logger.info(f"Email notification sent successfully: {subject} to {len(recipient_list)} recipients")
            else:
                logger.error(f"Failed to send email notification: {subject}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    @staticmethod
    def send_login_notification(user):
        """Send notification when user logs in"""
        subject = f"User Login Notification - {user.username}"
        
        message = f"""
        User Login Notification
        
        User: {user.get_full_name() or user.username}
        Email: {user.email}
        Username: {user.username}
        Time: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'N/A'}
        
        This is an automated notification from the pipsmade investment platform.
        """
        
        return EmailNotificationService.send_notification(
            subject=subject,
            message=message,
            notification_type='login'
        )
    
    @staticmethod
    def send_signup_notification(user):
        """Send notification when new user registers"""
        subject = f"New User Registration - {user.username}"
        
        message = f"""
        New User Registration
        
        User: {user.get_full_name() or user.username}
        Email: {user.email}
        Username: {user.username}
        Registration Date: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated notification from the pipsmade investment platform.
        """
        
        return EmailNotificationService.send_notification(
            subject=subject,
            message=message,
            notification_type='signup'
        )
    
    @staticmethod
    def send_deposit_notification(deposit_request):
        """Send notification when user makes deposit request"""
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
        
        return EmailNotificationService.send_notification(
            subject=subject,
            message=message,
            notification_type='deposits'
        )
    
    @staticmethod
    def send_withdrawal_notification(withdrawal_request):
        """Send notification when user makes withdrawal request"""
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
        
        return EmailNotificationService.send_notification(
            subject=subject,
            message=message,
            notification_type='withdrawals'
        )
    
    @staticmethod
    def send_support_notification(support_ticket):
        """Send notification when user submits support ticket"""
        subject = f"New Support Ticket - #{support_ticket.id}"
        
        message = f"""
        New Support Ticket
        
        Ticket ID: #{support_ticket.id}
        User: {support_ticket.user.get_full_name() or support_ticket.user.username}
        Email: {support_ticket.user.email}
        Category: {support_ticket.category.name}
        Priority: {support_ticket.priority}
        Subject: {support_ticket.subject}
        Message: {support_ticket.message[:200]}{'...' if len(support_ticket.message) > 200 else ''}
        Created: {support_ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        View in admin: /admin/support/supportticket/{support_ticket.id}/
        
        This is an automated notification from the pipsmade investment platform.
        """
        
        return EmailNotificationService.send_notification(
            subject=subject,
            message=message,
            notification_type='support'
        ) 