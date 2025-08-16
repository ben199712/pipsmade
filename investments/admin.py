from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from .models import InvestmentPlan, UserInvestment, InvestmentReturn, UserPortfolio, ManualProfit, AdminInvestmentPlan
from django.db import models
from django.contrib.auth import get_user_model

@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'min_investment', 'max_investment',
                   'min_roi_percentage', 'max_roi_percentage', 'duration_days', 'is_active']
    list_filter = ['plan_type', 'risk_level', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['plan_type', 'min_investment']

@admin.register(AdminInvestmentPlan)
class AdminInvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'roi_percentage', 'duration_days', 'risk_level', 'min_investment', 'created_by', 'is_active']
    list_filter = ['plan_type', 'risk_level', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Plan Details', {
            'fields': ('name', 'plan_type', 'description', 'is_active')
        }),
        ('Investment Parameters', {
            'fields': ('min_investment', 'max_investment', 'roi_percentage', 'duration_days', 'risk_level')
        }),
        ('Custom Features', {
            'fields': ('features', 'special_terms'),
            'classes': ('collapse',)
        }),
        ('Admin Info', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    actions = ['activate_plans', 'deactivate_plans', 'assign_to_users']
    
    def save_model(self, request, obj, form, change):
        """Set the admin who created the plan"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def activate_plans(self, request, queryset):
        """Activate selected plans"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Successfully activated {updated} plans.')
    
    activate_plans.short_description = "Activate selected plans"
    
    def deactivate_plans(self, request, queryset):
        """Deactivate selected plans"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Successfully deactivated {updated} plans.')
    
    deactivate_plans.short_description = "Deactivate selected plans"
    
    def assign_to_users(self, request, queryset):
        """Assign selected plans to users"""
        if len(queryset) != 1:
            self.message_user(request, 'Please select exactly one plan to assign to users.')
            return
        
        plan = queryset.first()
        return redirect('admin:assign_plan_to_users', plan_id=plan.id)
    
    assign_to_users.short_description = "Assign plan to users"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:plan_id>/assign-to-users/',
                self.admin_site.admin_view(self.assign_plan_to_users_view),
                name='assign_plan_to_users',
            ),
        ]
        return custom_urls + urls
    
    def assign_plan_to_users_view(self, request, plan_id):
        """View for assigning a plan to multiple users"""
        try:
            plan = AdminInvestmentPlan.objects.get(id=plan_id)
        except AdminInvestmentPlan.DoesNotExist:
            messages.error(request, 'Plan not found.')
            return redirect('admin:investments_admininvestmentplan_changelist')
        
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    user_ids = request.POST.getlist('user_ids')
                    investment_amount = Decimal(request.POST.get('investment_amount', plan.min_investment))
                    
                    if not user_ids:
                        messages.error(request, 'Please select at least one user.')
                        return redirect('admin:assign_plan_to_users', plan_id=plan.id)
                    
                    if investment_amount < plan.min_investment:
                        messages.error(request, f'Investment amount must be at least ${plan.min_investment}.')
                        return redirect('admin:assign_plan_to_users', plan_id=plan.id)
                    
                    if plan.max_investment and investment_amount > plan.max_investment:
                        messages.error(request, f'Investment amount cannot exceed ${plan.max_investment}.')
                        return redirect('admin:assign_plan_to_users', plan_id=plan.id)
                    
                    # Get users
                    User = get_user_model()
                    users = User.objects.filter(id__in=user_ids)
                    
                    created_count = 0
                    for user in users:
                        # Check if user already has this plan
                        existing_investment = UserInvestment.objects.filter(
                            user=user,
                            admin_investment_plan=plan,
                            status__in=['active', 'pending']
                        ).first()
                        
                        if existing_investment:
                            messages.warning(request, f'User {user.username} already has an active investment with this plan.')
                            continue
                        
                        # Create investment
                        investment = UserInvestment.objects.create(
                            user=user,
                            admin_investment_plan=plan,
                            amount=investment_amount,
                            roi_percentage=plan.roi_percentage,
                            status='active'
                        )
                        
                        # NO automatic portfolio updates - admin must update manually
                        # portfolio = UserPortfolio.get_or_create_portfolio(user)
                        # portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES
                        
                        created_count += 1
                    
                    if created_count > 0:
                        messages.success(
                            request, 
                            f'Successfully created {created_count} investments with plan "{plan.name}" for ${investment_amount} each.'
                        )
                        return redirect('admin:investments_admininvestmentplan_changelist')
                    else:
                        messages.warning(request, 'No new investments were created.')
                        
            except Exception as e:
                messages.error(request, f'Error creating investments: {str(e)}')
        
        # Get all users for selection
        User = get_user_model()
        users = User.objects.filter(is_active=True).exclude(is_superuser=True).order_by('username')
        
        # Get users who already have this plan
        existing_users = UserInvestment.objects.filter(
            admin_investment_plan=plan,
            status__in=['active', 'pending']
        ).values_list('user_id', flat=True)
        
        context = {
            'title': f'Assign Plan "{plan.name}" to Users',
            'plan': plan,
            'users': users,
            'existing_users': existing_users,
            'today': timezone.now().date(),
        }
        
        return render(request, 'admin/investments/assign_plan_to_users.html', context)

class InvestmentReturnInline(admin.TabularInline):
    """Inline editing for investment returns - ALL VALUES MANUAL"""
    model = InvestmentReturn
    extra = 1
    fields = ['date', 'daily_return', 'return_percentage', 'cumulative_return']
    # NO readonly fields - admin controls everything manually
    
    def get_queryset(self, request):
        """Show only recent returns"""
        qs = super().get_queryset(request)
        return qs.order_by('-date')
    
    def save_model(self, request, obj, form, change):
        """NO automatic calculations - admin controls everything"""
        super().save_model(request, obj, form, change)

@admin.register(UserInvestment)
class UserInvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_plan_name', 'get_plan_type', 'amount', 'roi_percentage', 'status', 'start_date', 'end_date', 'total_profit', 'total_withdrawable']
    list_filter = ['status', 'investment_plan__plan_type', 'admin_investment_plan__plan_type', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'investment_plan__name', 'admin_investment_plan__name']
    # NO readonly fields - admin controls everything manually
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'status')
        }),
        ('Investment Plan', {
            'fields': ('investment_plan', 'admin_investment_plan'),
            'description': 'Choose either a standard plan OR an admin-created custom plan (not both)'
        }),
        ('Investment Details', {
            'fields': ('amount', 'roi_percentage', 'start_date', 'end_date')
        }),
        ('MANUAL VALUES - Admin Controls Everything', {
            'fields': ('expected_return', 'current_value', 'manual_profit', 'total_profit', 'total_withdrawable'),
            'description': 'ADMIN MUST SET ALL VALUES MANUALLY - No automatic calculations'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [InvestmentReturnInline]
    
    actions = ['add_daily_return', 'bulk_add_returns', 'add_manual_profit', 'create_with_admin_plan']
    
    def get_plan_name(self, obj):
        """Display the plan name (standard or admin)"""
        return obj.get_plan_name()
    get_plan_name.short_description = 'Investment Plan'
    
    def get_plan_type(self, obj):
        """Display the plan type"""
        return obj.get_plan_type().title()
    get_plan_type.short_description = 'Plan Type'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Customize foreign key fields"""
        if db_field.name == "admin_investment_plan":
            kwargs["queryset"] = AdminInvestmentPlan.objects.filter(is_active=True)
        elif db_field.name == "investment_plan":
            kwargs["queryset"] = InvestmentPlan.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def clean(self):
        """Validate that only one plan type is selected"""
        from django.core.exceptions import ValidationError
        
        if self.cleaned_data.get('investment_plan') and self.cleaned_data.get('admin_investment_plan'):
            raise ValidationError("Cannot select both standard and admin investment plans. Choose one or the other.")
        
        if not self.cleaned_data.get('investment_plan') and not self.cleaned_data.get('admin_investment_plan'):
            raise ValidationError("Must select either a standard investment plan or an admin-created plan.")
    
    def create_with_admin_plan(self, request, queryset):
        """Create investment with admin plan for selected users"""
        if len(queryset) != 1:
            self.message_user(request, 'Please select exactly one investment to modify.')
            return
        
        investment = queryset.first()
        return redirect('admin:investments_userinvestment_change', investment.id)
    
    create_with_admin_plan.short_description = "Create investment with admin plan"
    
    def add_daily_return(self, request, queryset):
        """Add daily return for selected investments"""
        if len(queryset) != 1:
            self.message_user(request, 'Please select exactly one investment to add daily return.')
            return
        
        investment = queryset.first()
        return redirect('add_daily_return', investment_id=investment.id)
    
    add_daily_return.short_description = "Add daily return for selected investment"
    
    def bulk_add_returns(self, request, queryset):
        """Bulk add returns for selected investments"""
        if len(queryset) < 1:
            self.message_user(request, 'Please select at least one investment.')
            return
        
        investment_ids = ','.join(str(inv.id) for inv in queryset)
        return redirect('bulk_add_returns') + f'?investments={investment_ids}'
    
    bulk_add_returns.short_description = "Bulk add returns for selected investments"
    
    def refresh_portfolios(self, request, queryset):
        """Refresh portfolio metrics for selected users"""
        updated = 0
        for investment in queryset:
            investment.save()  # This will trigger portfolio update
            if investment.user.portfolio:
                investment.user.portfolio.update_portfolio_metrics()
                updated += 1
        
        self.message_user(request, f'Successfully refreshed {updated} portfolios.')
    
    refresh_portfolios.short_description = "Refresh portfolio metrics"
    
    def add_manual_profit(self, request, queryset):
        """Add manual profit to selected investments"""
        if len(queryset) != 1:
            self.message_user(request, 'Please select exactly one investment to add manual profit.')
            return
        
        investment = queryset.first()
        return redirect('admin:investments_userinvestment_change', investment.id)
    
    add_manual_profit.short_description = "Add manual profit to selected investment"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:investment_id>/add-daily-return/',
                self.admin_site.admin_view(self.add_daily_return_view),
                name='investments_userinvestment_add_daily_return',
            ),
            path(
                'bulk-add-returns/',
                self.admin_site.admin_view(self.bulk_add_returns_view),
                name='investments_userinvestment_bulk_add_returns',
            ),
        ]
        return custom_urls + urls
    
    def add_daily_return_view(self, request, investment_id):
        """View for adding daily return to a specific investment"""
        try:
            investment = UserInvestment.objects.get(id=investment_id)
        except UserInvestment.DoesNotExist:
            messages.error(request, 'Investment not found.')
            return redirect('admin:investments_userinvestment_changelist')
        
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    date_str = request.POST.get('date')
                    daily_return = Decimal(request.POST.get('daily_return', 0))
                    return_type = request.POST.get('return_type', 'profit')
                    
                    # Convert to negative if it's a loss
                    if return_type == 'loss':
                        daily_return = -abs(daily_return)
                    
                    # Get or create return record
                    return_obj, created = InvestmentReturn.objects.get_or_create(
                        investment=investment,
                        date=date_str,
                        defaults={
                            'daily_return': daily_return,
                            'return_percentage': (daily_return / investment.amount) * 100
                        }
                    )
                    
                    if not created:
                        return_obj.daily_return = daily_return
                        return_obj.return_percentage = (daily_return / investment.amount) * 100
                        return_obj.save()
                    
                    # Update cumulative return
                    total_returns = investment.returns.aggregate(total=models.Sum('daily_return'))['total'] or 0
                    return_obj.cumulative_return = total_returns
                    return_obj.save()
                    
                    # Update investment current value
                    investment.current_value = investment.amount + total_returns
                    investment.save()
                    
                    # Update user portfolio
                    portfolio = UserPortfolio.get_or_create_portfolio(investment.user)
                    portfolio.update_portfolio_metrics()
                    
                    messages.success(
                        request, 
                        f'Daily return of ${daily_return:,.2f} added for {investment.user.username} on {date_str}'
                    )
                    return redirect('admin:investments_userinvestment_changelist')
                    
            except Exception as e:
                messages.error(request, f'Error adding return: {str(e)}')
        
        # Get existing returns for this investment
        existing_returns = investment.returns.all().order_by('-date')[:10]
        
        context = {
            'title': f'Add Daily Return for {investment.user.username}',
            'investment': investment,
            'existing_returns': existing_returns,
            'today': timezone.now().date(),
        }
        
        return render(request, 'admin/investments/add_daily_return.html', context)
    
    def bulk_add_returns_view(self, request):
        """View for bulk adding returns to multiple investments"""
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    date_str = request.POST.get('date')
                    return_type = request.POST.get('return_type', 'profit')
                    return_amount = Decimal(request.POST.get('return_amount', 0))
                    
                    # Convert to negative if it's a loss
                    if return_type == 'loss':
                        return_amount = -abs(return_amount)
                    
                    # Get selected investment IDs
                    investment_ids = request.POST.getlist('investment_ids')
                    investments = UserInvestment.objects.filter(id__in=investment_ids, status='active')
                    
                    added_count = 0
                    for investment in investments:
                        # Calculate return based on investment amount (percentage)
                        daily_return = (return_amount / 100) * investment.amount
                        
                        # Get or create return record
                        return_obj, created = InvestmentReturn.objects.get_or_create(
                            investment=investment,
                            date=date_str,
                            defaults={
                                'daily_return': daily_return,
                                'return_percentage': return_amount
                            }
                        )
                        
                        if not created:
                            return_obj.daily_return = daily_return
                            return_obj.return_percentage = return_amount
                            return_obj.save()
                        
                        # Update cumulative return
                        total_returns = investment.returns.aggregate(total=models.Sum('daily_return'))['total'] or 0
                        return_obj.cumulative_return = total_returns
                        return_obj.save()
                        
                        # Update investment current value
                        investment.current_value = investment.amount + total_returns
                        investment.save()
                        
                        added_count += 1
                    
                    # Update portfolios for affected users
                    affected_users = set(investments.values_list('user_id', flat=True))
                    for user_id in affected_users:
                        portfolio = UserPortfolio.get_or_create_portfolio(get_user_model().objects.get(id=user_id))
                        portfolio.update_portfolio_metrics()
                    
                    messages.success(
                        request, 
                        f'Added {return_amount}% return to {added_count} investments on {date_str}'
                    )
                    return redirect('admin:investments_userinvestment_changelist')
                    
            except Exception as e:
                messages.error(request, f'Error adding returns: {str(e)}')
        
        # Get active investments for selection
        active_investments = UserInvestment.objects.filter(status='active').select_related('user', 'investment_plan')
        
        context = {
            'title': 'Bulk Add Returns',
            'active_investments': active_investments,
            'today': timezone.now().date(),
        }
        
        return render(request, 'admin/investments/bulk_add_returns.html', context)

@admin.register(InvestmentReturn)
class InvestmentReturnAdmin(admin.ModelAdmin):
    list_display = ['investment', 'date', 'daily_return', 'cumulative_return', 'return_percentage', 'user_info']
    list_filter = ['date', 'investment__investment_plan__plan_type', 'investment__status']
    search_fields = ['investment__user__username', 'investment__user__email']
    ordering = ['-date']
    readonly_fields = ['cumulative_return', 'created_at']
    
    def user_info(self, obj):
        """Display user information"""
        return f"{obj.investment.user.username} ({obj.investment.investment_plan.name})"
    user_info.short_description = 'User & Plan'
    
    def save_model(self, request, obj, form, change):
        """NO automatic calculations - admin controls everything"""
        super().save_model(request, obj, form, change)
        
        # NO automatic updates - admin must update everything manually
        # Update cumulative return for all subsequent returns
        # self.update_subsequent_returns(obj)  # REMOVED - NO AUTOMATIC UPDATES
        
        # Update investment current value
        # obj.investment.current_value = obj.investment.amount + obj.cumulative_return  # REMOVED - NO AUTOMATIC UPDATES
        # obj.investment.save()  # REMOVED - NO AUTOMATIC UPDATES
        
        # Update user portfolio
        # portfolio = UserPortfolio.get_or_create_portfolio(obj.investment.user)  # REMOVED - NO AUTOMATIC UPDATES
        # portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES

@admin.register(UserPortfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_invested', 'total_current_value', 'total_profit',
                   'total_roi_percentage', 'active_investments', 'last_updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_updated']
    ordering = ['-total_current_value']
    # NO actions - admin must update everything manually
    # actions = ['refresh_portfolios']  # REMOVED - NO AUTOMATIC UPDATES
    
    # def refresh_portfolios(self, request, queryset):  # REMOVED - NO AUTOMATIC UPDATES
    #     """Admin action to refresh portfolio metrics"""
    #     updated_count = 0
    #     for portfolio in queryset:
    #         portfolio.update_portfolio_metrics()
    #         updated_count += 1
    #     
    #     messages.success(request, f'Refreshed {updated_count} portfolios.')
    # refresh_portfolios.short_description = "Refresh Portfolio Metrics"

@admin.register(ManualProfit)
class ManualProfitAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'description', 'given_by', 'given_at', 'is_active']
    list_filter = ['is_active', 'given_at', 'given_by']
    search_fields = ['user__username', 'user__email', 'description']
    readonly_fields = ['given_at']
    ordering = ['-given_at']
    
    fieldsets = (
        ('Profit Details', {
            'fields': ('user', 'amount', 'description')
        }),
        ('Admin Info', {
            'fields': ('given_by', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('given_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_profits', 'deactivate_profits', 'refresh_portfolios']
    
    def save_model(self, request, obj, form, change):
        """Set the admin who gave the profit"""
        if not obj.given_by:
            obj.given_by = request.user
        super().save_model(request, obj, form, change)
        
        # NO automatic portfolio updates - admin must update manually
        # if obj.user.portfolio:  # REMOVED - NO AUTOMATIC UPDATES
        #     obj.user.portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES
    
    def activate_profits(self, request, queryset):
        """Activate selected profits"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Successfully activated {updated} profits.')
        
        # NO automatic portfolio updates - admin must update manually
        # for profit in queryset:  # REMOVED - NO AUTOMATIC UPDATES
        #     if profit.user.portfolio:  # REMOVED - NO AUTOMATIC UPDATES
        #         profit.user.portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES
    
    activate_profits.short_description = "Activate selected profits"
    
    def deactivate_profits(self, request, queryset):
        """Deactivate selected profits"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Successfully deactivated {updated} profits.')
        
        # NO automatic portfolio updates - admin must update manually
        # for profit in queryset:  # REMOVED - NO AUTOMATIC UPDATES
        #     if profit.user.portfolio:  # REMOVED - NO AUTOMATIC UPDATES
        #         profit.user.portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES
    
    deactivate_profits.short_description = "Deactivate selected profits"
    
    def refresh_portfolios(self, request, queryset):
        """Refresh portfolio metrics for users with selected profits"""
        # NO automatic portfolio updates - admin must update manually
        # updated = 0  # REMOVED - NO AUTOMATIC UPDATES
        # for profit in queryset:  # REMOVED - NO AUTOMATIC UPDATES
        #     if profit.user.portfolio:  # REMOVED - NO AUTOMATIC UPDATES
        #         profit.user.portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES
        #         updated += 1  # REMOVED - NO AUTOMATIC UPDATES
        # 
        # self.message_user(request, f'Successfully refreshed {updated} portfolios.')  # REMOVED - NO AUTOMATIC UPDATES
        
        self.message_user(request, 'Portfolio updates must be done manually by admin.')
    
    refresh_portfolios.short_description = "Portfolio updates must be manual"
