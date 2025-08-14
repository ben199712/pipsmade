from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class CryptoWallet(models.Model):
    """Admin-managed crypto wallet addresses"""
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('USDT', 'Tether (USDT)'),
        ('BNB', 'Binance Coin'),
        ('ADA', 'Cardano'),
        ('DOT', 'Polkadot'),
        ('LTC', 'Litecoin'),
        ('XRP', 'Ripple'),
        ('DOGE', 'Dogecoin'),
        ('MATIC', 'Polygon'),
    ]

    crypto_type = models.CharField(max_length=10, choices=CRYPTO_CHOICES, unique=True)
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50, help_text="e.g., ERC-20, BEP-20, TRC-20")
    is_active = models.BooleanField(default=True)
    minimum_deposit = models.DecimalField(max_digits=12, decimal_places=8, default=0.001)
    deposit_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    withdrawal_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['crypto_type']

    def __str__(self):
        return f"{self.get_crypto_type_display()} - {self.wallet_address[:20]}..."

    def get_crypto_icon(self):
        """Get Font Awesome icon for crypto"""
        icons = {
            'BTC': 'fab fa-bitcoin',
            'ETH': 'fab fa-ethereum',
            'USDT': 'fas fa-dollar-sign',
            'BNB': 'fas fa-coins',
            'ADA': 'fas fa-coins',
            'DOT': 'fas fa-circle',
            'LTC': 'fas fa-coins',
            'XRP': 'fas fa-water',
            'DOGE': 'fas fa-dog',
            'MATIC': 'fas fa-shapes',
        }
        return icons.get(self.crypto_type, 'fas fa-coins')

class UserWallet(models.Model):
    """User's wallet balance for different cryptocurrencies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    crypto_type = models.CharField(max_length=10, choices=CryptoWallet.CRYPTO_CHOICES)
    balance = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'crypto_type']
        ordering = ['crypto_type']

    def __str__(self):
        return f"{self.user.username} - {self.crypto_type}: {self.balance}"

class Transaction(models.Model):
    """All transactions (deposits, withdrawals, transfers)"""
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('investment', 'Investment'),
        ('profit', 'Profit'),
        ('fee', 'Fee'),
        ('bonus', 'Bonus'),
        ('refund', 'Refund'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    # Basic Info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Amount Info
    amount = models.DecimalField(max_digits=18, decimal_places=8, validators=[MinValueValidator(Decimal('0.00000001'))])
    crypto_type = models.CharField(max_length=10, choices=CryptoWallet.CRYPTO_CHOICES)
    usd_equivalent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Transaction Details
    transaction_hash = models.CharField(max_length=255, null=True, blank=True)
    from_address = models.CharField(max_length=255, null=True, blank=True)
    to_address = models.CharField(max_length=255, null=True, blank=True)

    # Fees
    network_fee = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    platform_fee = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    # Admin & Notes
    admin_notes = models.TextField(blank=True)
    user_notes = models.TextField(blank=True)

    # Approval Workflow
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transactions')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_type', 'status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} - {self.amount} {self.crypto_type}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def get_status_color(self):
        """Get Bootstrap color class for status"""
        colors = {
            'pending': 'warning',
            'processing': 'info',
            'completed': 'success',
            'failed': 'danger',
            'cancelled': 'secondary',
            'rejected': 'danger',
        }
        return colors.get(self.status, 'secondary')

    def get_type_icon(self):
        """Get Font Awesome icon for transaction type"""
        icons = {
            'deposit': 'fas fa-arrow-down',
            'withdrawal': 'fas fa-arrow-up',
            'investment': 'fas fa-chart-line',
            'profit': 'fas fa-dollar-sign',
            'fee': 'fas fa-minus',
            'bonus': 'fas fa-gift',
            'refund': 'fas fa-undo',
        }
        return icons.get(self.transaction_type, 'fas fa-exchange-alt')

    def net_amount(self):
        """Calculate net amount after fees"""
        return self.amount - self.network_fee - self.platform_fee

    def has_deposit_request(self):
        """Check if transaction has associated deposit request"""
        return hasattr(self, 'deposit_request')

    def has_withdrawal_request(self):
        """Check if transaction has associated withdrawal request"""
        return hasattr(self, 'withdrawal_request')

class DepositRequest(models.Model):
    """User deposit requests with proof of payment"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit_requests')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='deposit_request')

    # Deposit Details
    crypto_wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=8, validators=[MinValueValidator(Decimal('0.00000001'))])

    # Proof of Payment
    transaction_hash = models.CharField(max_length=255, help_text="Blockchain transaction hash")
    proof_image = models.ImageField(upload_to='deposit_proofs/', null=True, blank=True, help_text="Screenshot of transaction")
    sender_address = models.CharField(max_length=255, help_text="Address you sent from")

    # Admin Review
    admin_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_deposits')
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Deposit: {self.user.username} - {self.amount} {self.crypto_wallet.crypto_type}"

class WithdrawalRequest(models.Model):
    """User withdrawal requests"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='withdrawal_request')

    # Withdrawal Details
    crypto_type = models.CharField(max_length=10, choices=CryptoWallet.CRYPTO_CHOICES)
    amount = models.DecimalField(max_digits=18, decimal_places=8, validators=[MinValueValidator(Decimal('0.00000001'))])
    destination_address = models.CharField(max_length=255, help_text="Address to send crypto to")
    network = models.CharField(max_length=50, help_text="Network (e.g., ERC-20, BEP-20)")

    # Fees
    network_fee = models.DecimalField(max_digits=18, decimal_places=8, default=0)
    platform_fee = models.DecimalField(max_digits=18, decimal_places=8, default=0)

    # Security
    two_factor_verified = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    # Admin Processing
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_withdrawals')
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_notes = models.TextField(blank=True)

    # Blockchain Info (filled after processing)
    sent_transaction_hash = models.CharField(max_length=255, null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Withdrawal: {self.user.username} - {self.amount} {self.crypto_type}"

    def net_amount(self):
        """Amount user will receive after fees"""
        return self.amount - self.network_fee - self.platform_fee

class TransactionNotification(models.Model):
    """Notifications for transaction status changes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_notifications')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='notifications')

    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('deposit_confirmed', 'Deposit Confirmed'),
        ('withdrawal_approved', 'Withdrawal Approved'),
        ('withdrawal_rejected', 'Withdrawal Rejected'),
        ('withdrawal_completed', 'Withdrawal Completed'),
        ('transaction_failed', 'Transaction Failed'),
    ])

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
