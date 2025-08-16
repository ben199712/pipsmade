from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    CryptoWallet, UserWallet, Transaction,
    DepositRequest, WithdrawalRequest, TransactionNotification
)

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = [
        'crypto_type', 'wallet_address_short', 'network', 'is_active',
        'minimum_deposit', 'withdrawal_fee_percentage', 'created_at'
    ]
    list_filter = ['crypto_type', 'is_active', 'network']
    search_fields = ['crypto_type', 'wallet_address', 'network']
    ordering = ['crypto_type']

    fieldsets = (
        ('Basic Information', {
            'fields': ('crypto_type', 'wallet_address', 'network', 'is_active')
        }),
        ('Deposit Settings', {
            'fields': ('minimum_deposit', 'deposit_fee_percentage')
        }),
        ('Withdrawal Settings', {
            'fields': ('withdrawal_fee_percentage',)
        }),
    )

    def wallet_address_short(self, obj):
        return f"{obj.wallet_address[:20]}..." if len(obj.wallet_address) > 20 else obj.wallet_address
    wallet_address_short.short_description = 'Wallet Address'

@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'crypto_type', 'balance', 'updated_at']
    list_filter = ['crypto_type', 'updated_at']
    search_fields = ['user__username', 'user__email', 'crypto_type']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'transaction_type', 'amount', 'crypto_type',
        'status_badge', 'created_at', 'admin_actions'
    ]
    list_filter = [
        'transaction_type', 'status', 'crypto_type', 'created_at',
        'approved_by'
    ]
    search_fields = [
        'user__username', 'user__email', 'transaction_hash',
        'from_address', 'to_address'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'completed_at', 'net_amount_display'
    ]
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'user', 'transaction_type', 'status', 'amount', 'crypto_type'
            )
        }),
        ('Transaction Details', {
            'fields': (
                'transaction_hash', 'from_address', 'to_address',
                'network_fee', 'platform_fee', 'net_amount_display'
            )
        }),
        ('Notes', {
            'fields': ('user_notes', 'admin_notes')
        }),
        ('Approval Information', {
            'fields': (
                'approved_by', 'approved_at', 'rejection_reason'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )

    def status_badge(self, obj):
        color = obj.get_status_color()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def net_amount_display(self, obj):
        return f"{obj.net_amount()} {obj.crypto_type}"
    net_amount_display.short_description = 'Net Amount'

    def admin_actions(self, obj):
        if obj.status == 'pending':
            if obj.transaction_type == 'deposit' and obj.has_deposit_request():
                try:
                    deposit_request = obj.deposit_request
                    url = reverse('admin_approve_deposit', args=[deposit_request.id])
                    return format_html('<a href="{}" class="btn btn-sm btn-primary">Review</a>', url)
                except:
                    return format_html('<span class="text-muted">No deposit request</span>')
            elif obj.transaction_type == 'withdrawal' and obj.has_withdrawal_request():
                try:
                    withdrawal_request = obj.withdrawal_request
                    url = reverse('admin_process_withdrawal', args=[withdrawal_request.id])
                    return format_html('<a href="{}" class="btn btn-sm btn-warning">Process</a>', url)
                except:
                    return format_html('<span class="text-muted">No withdrawal request</span>')
            else:
                return format_html('<span class="text-muted">Pending</span>')
        return format_html('<span class="badge bg-{}">{}</span>', obj.get_status_color(), obj.get_status_display())
    admin_actions.short_description = 'Actions'

@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'crypto_wallet', 'amount', 'transaction_hash_short',
        'admin_verified', 'created_at', 'admin_actions'
    ]
    list_filter = ['admin_verified', 'crypto_wallet__crypto_type', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'transaction_hash',
        'sender_address'
    ]
    readonly_fields = ['created_at', 'updated_at', 'verified_at', 'proof_image_display']

    fieldsets = (
        ('Deposit Information', {
            'fields': (
                'user', 'crypto_wallet', 'amount', 'transaction_hash',
                'sender_address'
            )
        }),
        ('Proof of Payment', {
            'fields': ('proof_image',)
        }),
        ('Admin Verification', {
            'fields': (
                'admin_verified', 'verification_notes', 'verified_by',
                'verified_at'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def transaction_hash_short(self, obj):
        return f"{obj.transaction_hash[:20]}..." if len(obj.transaction_hash) > 20 else obj.transaction_hash
    transaction_hash_short.short_description = 'Transaction Hash'

    def proof_image_display(self, obj):
        if obj.proof_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.proof_image.url
            )
        return 'No image uploaded'
    proof_image_display.short_description = 'Proof Image'

    def admin_actions(self, obj):
        if not obj.admin_verified:
            try:
                url = reverse('admin_approve_deposit', args=[obj.id])
                return format_html('<a href="{}" class="btn btn-sm btn-primary">Review</a>', url)
            except:
                return format_html('<span class="text-muted">Review</span>')
        return format_html('<span class="badge bg-success">Verified</span>')
    admin_actions.short_description = 'Actions'

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'crypto_type', 'amount', 'destination_address_short',
        'transaction_status', 'created_at', 'admin_actions'
    ]
    list_filter = ['crypto_type', 'network', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'destination_address',
        'sent_transaction_hash'
    ]
    readonly_fields = ['created_at', 'updated_at', 'processed_at', 'sent_at']

    def destination_address_short(self, obj):
        return f"{obj.destination_address[:20]}..." if len(obj.destination_address) > 20 else obj.destination_address
    destination_address_short.short_description = 'Destination'

    def transaction_status(self, obj):
        return obj.transaction.get_status_display()
    transaction_status.short_description = 'Status'

    def admin_actions(self, obj):
        if obj.transaction.status == 'pending':
            try:
                url = reverse('admin_process_withdrawal', args=[obj.id])
                return format_html('<a href="{}" class="btn btn-sm btn-warning">Process</a>', url)
            except:
                return format_html('<span class="text-muted">Process</span>')
        return format_html('<span class="badge bg-{}">{}</span>',
                          obj.transaction.get_status_color(),
                          obj.transaction.get_status_display())
    admin_actions.short_description = 'Actions'

@admin.register(TransactionNotification)
class TransactionNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
