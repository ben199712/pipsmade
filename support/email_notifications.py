"""
Simple email notification system for support
"""
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_support_notification(support_ticket):
    """Send notification when user submits support ticket"""
    try:
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
            logger.info(f"Support notification sent successfully to {admin_email}")
        else:
            logger.error(f"Failed to send support notification to {admin_email}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending support notification: {e}")
        return False 