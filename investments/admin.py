from django.contrib import admin
from .models import InvestmentPlan, UserInvestment, InvestmentReturn, UserPortfolio

@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'min_investment', 'max_investment',
                   'min_roi_percentage', 'max_roi_percentage', 'duration_days', 'is_active']
    list_filter = ['plan_type', 'risk_level', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['plan_type', 'min_investment']

@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'investment_plan', 'amount', 'roi_percentage',
                   'status', 'start_date', 'end_date', 'current_value']
    list_filter = ['status', 'investment_plan__plan_type', 'start_date']
    search_fields = ['user__username', 'user__email', 'investment_plan__name']
    readonly_fields = ['current_value', 'expected_return', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(InvestmentReturn)
class InvestmentReturnAdmin(admin.ModelAdmin):
    list_display = ['investment', 'date', 'daily_return', 'cumulative_return', 'return_percentage']
    list_filter = ['date', 'investment__investment_plan__plan_type']
    search_fields = ['investment__user__username']
    ordering = ['-date']

@admin.register(UserPortfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_invested', 'total_current_value', 'total_profit',
                   'total_roi_percentage', 'active_investments', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']
    ordering = ['-total_current_value']
