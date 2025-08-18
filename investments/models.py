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

class AdminInvestmentPlan(models.Model):
    """Custom investment plans created by admin for specific users"""
    PLAN_TYPES = [
        ('crypto', 'Cryptocurrency'),
        ('stocks', 'Stock Market'),
        ('forex', 'Forex Trading'),
        ('bonds', 'Bonds & Fixed Income'),
        ('custom', 'Custom Plan'),
    ]

    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]

    # Plan Details
    name = models.CharField(max_length=100, help_text="Custom name for this investment plan")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='custom')
    description = models.TextField(help_text="Description of this custom plan")
    
    # Investment Parameters
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # ROI Configuration
    roi_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Fixed ROI percentage for this plan"
    )
    
    # Duration
    duration_days = models.PositiveIntegerField(default=30, help_text="Duration in days")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='medium')
    
    # Admin Info
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_plans', help_text="Admin who created this plan")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether this plan is active")
    
    # Custom Features
    features = models.JSONField(default=list, blank=True, help_text="Custom features for this plan")
    special_terms = models.TextField(blank=True, help_text="Special terms and conditions")
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()}) - {self.roi_percentage}% ROI"
    
    def get_average_roi(self):
        """Get ROI percentage (same as roi_percentage for admin plans)"""
        return self.roi_percentage
    
    def calculate_potential_return(self, amount):
        """Calculate potential return for given amount"""
        return amount * (self.roi_percentage / 100)

class UserInvestment(models.Model):
    """User's active investments"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, null=True, blank=True, help_text="Standard investment plan")
    admin_investment_plan = models.ForeignKey(AdminInvestmentPlan, on_delete=models.CASCADE, null=True, blank=True, help_text="Admin-created custom investment plan")
    
    # Investment Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # Dates
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # MANUAL FIELDS - Admin controls everything
    expected_return = models.DecimalField(max_digits=12, decimal_places=2, help_text="Set manually by admin")
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Set manually by admin")
    
    # Manual profit entry by admin
    manual_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Profit added manually by admin")
    total_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Set manually by admin")
    total_withdrawable = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Set manually by admin")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        plan_name = self.investment_plan.name if self.investment_plan else self.admin_investment_plan.name
        return f"{self.user.username} - {plan_name} - ${self.amount}"

    def get_plan_name(self):
        """Get the name of the investment plan (standard or admin-created)"""
        if self.investment_plan:
            return self.investment_plan.name
        elif self.admin_investment_plan:
            return self.admin_investment_plan.name
        return "Unknown Plan"
    
    def get_plan_type(self):
        """Get the type of the investment plan"""
        if self.investment_plan:
            return self.investment_plan.plan_type
        elif self.admin_investment_plan:
            return self.admin_investment_plan.plan_type
        return "unknown"

    def save(self, *args, **kwargs):
        print(f"DEBUG: UserInvestment.save() called for user: {self.user.username if self.user else 'None'}")
        print(f"DEBUG: start_date: {self.start_date}")
        print(f"DEBUG: end_date: {self.end_date}")
        print(f"DEBUG: investment_plan: {self.investment_plan}")
        print(f"DEBUG: admin_investment_plan: {self.admin_investment_plan}")
        
        # Ensure only one plan type is set
        if self.investment_plan and self.admin_investment_plan:
            raise ValueError("Cannot have both standard and admin investment plans")
        
        if not self.investment_plan and not self.admin_investment_plan:
            raise ValueError("Must have either standard or admin investment plan")
        
        # Ensure start_date is set (it should be auto_now_add=True, but let's be safe)
        if not self.start_date:
            from django.utils import timezone
            self.start_date = timezone.now()
            print(f"DEBUG: Set start_date to: {self.start_date}")
        
        # Set end date based on plan duration (only if not set)
        if not self.end_date:
            if self.investment_plan:
                self.end_date = self.start_date + timedelta(days=self.investment_plan.duration_days)
                print(f"DEBUG: Set end_date to: {self.end_date} (plan duration: {self.investment_plan.duration_days} days)")
            elif self.admin_investment_plan:
                self.end_date = self.start_date + timedelta(days=self.admin_investment_plan.duration_days)
                print(f"DEBUG: Set end_date to: {self.end_date} (admin plan duration: {self.admin_investment_plan.duration_days} days)")

        # Set ROI percentage from plan if not specified (only if not set)
        if not self.roi_percentage:
            if self.investment_plan:
                self.roi_percentage = self.investment_plan.get_average_roi()
                print(f"DEBUG: Set roi_percentage to: {self.roi_percentage}%")
            elif self.admin_investment_plan:
                self.roi_percentage = self.admin_investment_plan.roi_percentage
                print(f"DEBUG: Set roi_percentage to: {self.roi_percentage}%")

        print(f"DEBUG: About to call super().save()")
        # NO AUTOMATIC CALCULATIONS - Admin controls everything
        super().save(*args, **kwargs)
        print(f"DEBUG: UserInvestment saved successfully with ID: {self.id}")

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

    def get_profit(self):
        """Get current profit for the investment"""
        return self.total_profit or Decimal('0')

    def get_current_value(self):
        """Get current value of the investment"""
        return self.current_value or self.amount

    def get_expected_return(self):
        """Get expected return amount"""
        if self.expected_return:
            return self.expected_return
        # Calculate based on ROI if expected_return not set
        return self.amount * (self.roi_percentage / 100)

class InvestmentReturn(models.Model):
    """Track daily returns for investments - ALL VALUES SET MANUALLY BY ADMIN"""
    investment = models.ForeignKey(UserInvestment, on_delete=models.CASCADE, related_name='returns')
    date = models.DateField()
    daily_return = models.DecimalField(max_digits=12, decimal_places=2, help_text="Set manually by admin")
    cumulative_return = models.DecimalField(max_digits=12, decimal_places=2, help_text="Set manually by admin")
    return_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Set manually by admin")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['investment', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.investment} - {self.date} - {self.return_percentage}%"
    
    def save(self, *args, **kwargs):
        """NO AUTOMATIC CALCULATIONS - Admin controls everything"""
        # Admin must set cumulative_return manually
        super().save(*args, **kwargs)

class ManualProfit(models.Model):
    """Manual profit entries given by admin without requiring investments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manual_profits')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Profit amount to give to user")
    description = models.CharField(max_length=255, help_text="Reason for giving this profit")
    given_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profits_given', help_text="Admin who gave this profit")
    given_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether this profit is still active")
    
    class Meta:
        ordering = ['-given_at']
        
    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.description}"

class UserPortfolio(models.Model):
    """User's portfolio summary - ALL VALUES SET MANUALLY BY ADMIN"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')

    # MANUAL PORTFOLIO METRICS - Admin controls everything
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Set manually by admin")
    total_current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Set manually by admin")
    total_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Set manually by admin")
    total_roi_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Set manually by admin")
    
    # Total withdrawable amount
    total_withdrawable = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Set manually by admin")
    
    # Manual profit tracking
    manual_profit_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Set manually by admin")

    # Investment counts - Set manually by admin
    active_investments = models.PositiveIntegerField(default=0, help_text="Set manually by admin")
    completed_investments = models.PositiveIntegerField(default=0, help_text="Set manually by admin")

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    def update_portfolio_metrics(self):
        """NO AUTOMATIC UPDATES - Admin must update manually"""
        # This method does nothing - admin controls all values
        pass

    @classmethod
    def get_or_create_portfolio(cls, user):
        """Get or create portfolio for user - no automatic updates"""
        portfolio, created = cls.objects.get_or_create(user=user)
        # NO automatic updates - admin must set all values manually
        return portfolio
