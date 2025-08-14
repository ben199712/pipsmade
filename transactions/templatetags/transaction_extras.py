from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def admin_action_button(transaction):
    """Generate admin action button for transaction"""
    if transaction.status != 'pending':
        return mark_safe(f'<span class="badge bg-{transaction.get_status_color()}">{transaction.get_status_display()}</span>')
    
    if transaction.transaction_type == 'deposit':
        if transaction.has_deposit_request():
            try:
                url = reverse('admin_approve_deposit', args=[transaction.deposit_request.id])
                return mark_safe(f'<a href="{url}" class="btn btn-sm btn-success"><i class="fas fa-check"></i> Review</a>')
            except:
                return mark_safe('<span class="badge bg-secondary">No Request</span>')
        else:
            return mark_safe('<span class="badge bg-secondary">No Request</span>')
    
    elif transaction.transaction_type == 'withdrawal':
        if transaction.has_withdrawal_request():
            try:
                url = reverse('admin_process_withdrawal', args=[transaction.withdrawal_request.id])
                return mark_safe(f'<a href="{url}" class="btn btn-sm btn-warning"><i class="fas fa-cog"></i> Process</a>')
            except:
                return mark_safe('<span class="badge bg-secondary">No Request</span>')
        else:
            return mark_safe('<span class="badge bg-secondary">No Request</span>')
    
    else:
        return mark_safe('<span class="badge bg-info">Pending</span>')

@register.filter
def get_request_id(transaction, request_type):
    """Get request ID for transaction"""
    try:
        if request_type == 'deposit' and transaction.has_deposit_request():
            return transaction.deposit_request.id
        elif request_type == 'withdrawal' and transaction.has_withdrawal_request():
            return transaction.withdrawal_request.id
    except:
        pass
    return None
