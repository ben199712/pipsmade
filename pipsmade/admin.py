from django.contrib import admin
from .models import AdminEmailConfig

@admin.register(AdminEmailConfig)
class AdminEmailConfigAdmin(admin.ModelAdmin):
    """Admin interface for email configuration"""
    
    list_display = [
        'admin_user', 
        'email_address', 
        'notify_login', 
        'notify_signup', 
        'notify_deposits', 
        'notify_withdrawals', 
        'notify_support',
        'updated_at'
    ]
    
    list_filter = [
        'notify_login', 
        'notify_signup', 
        'notify_deposits', 
        'notify_withdrawals', 
        'notify_support',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'admin_user__username', 
        'admin_user__email', 
        'email_address'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Admin User', {
            'fields': ('admin_user', 'email_address')
        }),
        ('Notification Preferences', {
            'fields': (
                'notify_login', 
                'notify_signup', 
                'notify_deposits', 
                'notify_withdrawals', 
                'notify_support'
            ),
            'description': 'Select which types of notifications this admin should receive'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Only show configs for staff users"""
        return super().get_queryset(request).filter(admin_user__is_staff=True) 