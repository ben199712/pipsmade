from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Sum

class InvestmentPlan(models.Model):
    """Investment plans available to users"""
    PLAN_TYPES = [
        ('crypto', 'Cryptocurrency'),
        ('stocks', 'Stock Market'),
        ('forex', 'Forex Trading'),
        ('bonds', 'Bonds & Fixed Income'),
    ]

    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # ROI Configuration
    min_roi_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_roi_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Duration in days
    duration_days = models.PositiveIntegerField(default=30)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='medium')

    # Features
    features = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['plan_type', 'min_investment']

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"

    def get_average_roi(self):
        """Calculate average ROI percentage"""
        return (self.min_roi_percentage + self.max_roi_percentage) / 2

    def calculate_potential_return(self, amount):
        """Calculate potential return for given amount"""
        avg_roi = self.get_average_roi()
        return amount * (avg_roi / 100)

class UserInvestment(models.Model):
    """User's active investments"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)

    # Investment Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # Dates
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Calculated fields
    expected_return = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.investment_plan.name} - ${self.amount}"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.investment_plan.duration_days)

        if not self.expected_return:
            self.expected_return = self.amount * (self.roi_percentage / 100)

        # Update current value based on progress
        self.update_current_value()

        super().save(*args, **kwargs)

    def update_current_value(self):
        """Update current value based on time progress and ROI"""
        if self.status != 'active':
            return

        now = timezone.now()
        total_duration = (self.end_date - self.start_date).total_seconds()
        elapsed_duration = (now - self.start_date).total_seconds()

        if elapsed_duration <= 0:
            progress = 0
        elif elapsed_duration >= total_duration:
            progress = 1
            self.status = 'completed'
        else:
            progress = elapsed_duration / total_duration

        # Calculate current value with compound interest simulation
        self.current_value = self.amount + (self.expected_return * Decimal(str(progress)))

    def get_profit(self):
        """Get current profit"""
        return self.current_value - self.amount

    def get_progress_percentage(self):
        """Get investment progress as percentage"""
        if self.status == 'completed':
            return 100

        now = timezone.now()
        total_duration = (self.end_date - self.start_date).total_seconds()
        elapsed_duration = (now - self.start_date).total_seconds()

        if elapsed_duration <= 0:
            return 0
        elif elapsed_duration >= total_duration:
            return 100
        else:
            return (elapsed_duration / total_duration) * 100

    def days_remaining(self):
        """Get days remaining for investment"""
        if self.status == 'completed':
            return 0

        now = timezone.now()
        remaining = self.end_date - now
        return max(0, remaining.days)

    def is_mature(self):
        """Check if investment has matured"""
        return timezone.now() >= self.end_date

class InvestmentReturn(models.Model):
    """Track daily returns for investments"""
    investment = models.ForeignKey(UserInvestment, on_delete=models.CASCADE, related_name='returns')
    date = models.DateField()
    daily_return = models.DecimalField(max_digits=12, decimal_places=2)
    cumulative_return = models.DecimalField(max_digits=12, decimal_places=2)
    return_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['investment', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.investment} - {self.date} - {self.return_percentage}%"

class UserPortfolio(models.Model):
    """User's portfolio summary"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')

    # Portfolio metrics
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_roi_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Investment counts
    active_investments = models.PositiveIntegerField(default=0)
    completed_investments = models.PositiveIntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    def update_portfolio_metrics(self):
        """Update portfolio metrics based on user investments"""
        investments = self.user.investments.all()

        # Calculate totals
        self.total_invested = sum(inv.amount for inv in investments)
        self.total_current_value = sum(inv.current_value for inv in investments)
        self.total_profit = self.total_current_value - self.total_invested

        # Calculate ROI percentage
        if self.total_invested > 0:
            self.total_roi_percentage = (self.total_profit / self.total_invested) * 100
        else:
            self.total_roi_percentage = 0

        # Count investments by status
        self.active_investments = investments.filter(status='active').count()
        self.completed_investments = investments.filter(status='completed').count()

        self.save()

    @classmethod
    def get_or_create_portfolio(cls, user):
        """Get or create portfolio for user"""
        portfolio, created = cls.objects.get_or_create(user=user)
        if created or not portfolio.last_updated:
            portfolio.update_portfolio_metrics()
        return portfolio
