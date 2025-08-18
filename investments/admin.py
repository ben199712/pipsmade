from django.contrib import admin
from django import forms
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import InvestmentPlan, UserInvestment, UserPortfolio, InvestmentReturn, AdminInvestmentPlan

class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_plan_name', 'amount', 'roi_percentage', 'status', 'created_at', 'current_value']
    list_filter = ['status', 'created_at', 'investment_plan__plan_type']
    search_fields = ['user__username', 'user__email', 'investment_plan__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_plan_name(self, obj):
        if obj.investment_plan:
            return f"{obj.investment_plan.name} ({obj.investment_plan.plan_type})"
        elif obj.admin_investment_plan:
            return f"{obj.admin_investment_plan.name} (Admin Plan)"
        return "No Plan"
    get_plan_name.short_description = 'Investment Plan'

class InvestmentReturnAdmin(admin.ModelAdmin):
    list_display = ['investment', 'date', 'daily_return', 'cumulative_return', 'return_percentage']
    list_filter = ['date', 'investment__status']
    search_fields = ['investment__user__username', 'investment__investment_plan__name']
    readonly_fields = ['created_at']

class UserPortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_invested', 'total_current_value', 'total_profit', 'total_roi_percentage', 'total_withdrawable', 'active_investments']
    list_filter = ['last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

class AdminInvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'min_investment', 'max_investment', 'roi_percentage', 'duration_days', 'is_active']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

# Register the models
admin.site.register(InvestmentPlan, admin.ModelAdmin)
admin.site.register(UserInvestment, UserInvestmentAdmin)
admin.site.register(UserPortfolio, UserPortfolioAdmin)
admin.site.register(InvestmentReturn, InvestmentReturnAdmin)
admin.site.register(AdminInvestmentPlan, AdminInvestmentPlanAdmin)
