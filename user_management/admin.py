from django.contrib import admin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from investments.models import UserPortfolio, UserInvestment, InvestmentPlan
from .models import UserManagementProxy

User = get_user_model()

class UserManagementAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_management_change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        # Get statistics for the dashboard
        from django.db.models import Sum, Count
        
        total_users = User.objects.filter(is_active=True).count()
        active_investments = UserInvestment.objects.filter(status='active').count()
        
        # Get portfolio statistics
        portfolio_stats = UserPortfolio.objects.aggregate(
            total_value=Sum('total_current_value'),
            total_profits=Sum('total_profit')
        )
        
        total_portfolio_value = portfolio_stats.get('total_value', 0) or 0
        total_profits = portfolio_stats.get('total_profits', 0) or 0
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_users': total_users,
            'active_investments': active_investments,
            'total_portfolio_value': total_portfolio_value,
            'total_profits': total_profits,
        })
        
        return super().changelist_view(request, extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('assign-plan/', self.assign_plan_view, name='user_management_usermanagementproxy_assign_plan'),
            path('add-profit/', self.add_profit_view, name='user_management_usermanagementproxy_add_profit'),
            path('quick-actions/', self.quick_actions_view, name='user_management_usermanagementproxy_quick_actions'),
        ]
        return custom_urls + urls
    
    def assign_plan_view(self, request):
        if request.method == 'POST':
            user_id = request.POST.get('user')
            plan_id = request.POST.get('plan')
            amount = request.POST.get('amount')
            roi_percentage = request.POST.get('roi_percentage')
            notes = request.POST.get('notes', '')
            
            if user_id and plan_id and amount:
                try:
                    from decimal import Decimal
                    
                    user = User.objects.get(id=user_id)
                    plan = InvestmentPlan.objects.get(id=plan_id)
                    amount = Decimal(amount)
                    roi_percentage = Decimal(roi_percentage) if roi_percentage else Decimal('0')
                    
                    # Create the investment
                    from django.utils import timezone
                    from datetime import timedelta
                    
                    try:
                        # Calculate end date based on plan duration
                        start_date = timezone.now()
                        if hasattr(plan, 'duration_days') and plan.duration_days:
                            end_date = start_date + timedelta(days=plan.duration_days)
                        else:
                            end_date = start_date + timedelta(days=30)  # Default 30 days
                        
                        # Calculate expected return
                        if roi_percentage:
                            expected_return = amount * (roi_percentage / 100)
                        else:
                            # Use plan's default ROI if available
                            if hasattr(plan, 'get_average_roi'):
                                expected_return = amount * (plan.get_average_roi() / 100)
                            else:
                                expected_return = amount * 0.05  # Default 5% ROI
                        
                        investment = UserInvestment.objects.create(
                            user=user,
                            investment_plan=plan,
                            amount=amount,
                            roi_percentage=roi_percentage or (plan.get_average_roi() if hasattr(plan, 'get_average_roi') else 5.0),
                            status='active',
                            start_date=start_date,
                            end_date=end_date,
                            expected_return=expected_return,
                            current_value=amount,
                            total_withdrawable=amount
                        )
                        
                        messages.success(request, f'Successfully assigned {plan.name} plan to {user.username} with ${amount}')
                        
                    except Exception as e:
                        messages.error(request, f'Error creating investment: {str(e)}')
                        return redirect('admin:user_management_usermanagementproxy_changelist')
                    
                    # Update user portfolio
                    portfolio, created = UserPortfolio.objects.get_or_create(
                        user=user,
                        defaults={
                            'total_invested': amount,
                            'total_current_value': amount,
                            'total_profit': 0,
                            'total_roi_percentage': 0,
                            'total_withdrawable': amount,
                            'active_investments': 1
                        }
                    )
                    
                    if not created:
                        portfolio.total_invested += amount
                        portfolio.total_current_value += amount
                        portfolio.total_withdrawable += amount
                        portfolio.active_investments += 1
                        portfolio.save()
                    
                    return redirect('admin:user_management_usermanagementproxy_changelist')
                    
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
            else:
                messages.error(request, 'Please fill in all required fields')
        
        # Get users and plans for the form
        users = User.objects.filter(is_active=True).order_by('username')
        plans = InvestmentPlan.objects.filter(is_active=True).order_by('name')
        
        context = {
            'title': 'Assign Investment Plan to User',
            'users': users,
            'plans': plans,
        }
        return TemplateResponse(request, 'admin/assign_plan.html', context)
    
    def add_profit_view(self, request):
        if request.method == 'POST':
            user_id = request.POST.get('user')
            profit_amount = request.POST.get('profit_amount')
            profit_type = request.POST.get('profit_type')
            notes = request.POST.get('notes', '')
            
            if user_id and profit_amount:
                try:
                    from decimal import Decimal
                    from transactions.models import Transaction
                    
                    user = User.objects.get(id=user_id)
                    profit_amount = Decimal(profit_amount)
                    
                    # Get or create user portfolio
                    portfolio, created = UserPortfolio.objects.get_or_create(
                        user=user,
                        defaults={
                            'total_invested': 0,
                            'total_current_value': profit_amount,
                            'total_profit': profit_amount,
                            'total_roi_percentage': 0,
                            'total_withdrawable': profit_amount,
                            'active_investments': 0,
                            'manual_profit_total': profit_amount
                        }
                    )
                    
                    if not created:
                        portfolio.total_profit += profit_amount
                        portfolio.total_current_value += profit_amount
                        portfolio.total_withdrawable += profit_amount
                        portfolio.manual_profit_total += profit_amount
                        
                        # Recalculate ROI if there are investments
                        if portfolio.total_invested > 0:
                            portfolio.total_roi_percentage = (portfolio.total_profit / portfolio.total_invested) * 100
                        
                        portfolio.save()
                    
                    # Create a transaction record for the profit
                    Transaction.objects.create(
                        user=user,
                        transaction_type='profit',
                        amount=profit_amount,
                        usd_equivalent=profit_amount,
                        status='completed',
                        crypto_type='USD',
                        admin_notes=f'Manual profit added by admin: {notes}',
                        approved_by=request.user,
                        approved_at=timezone.now()
                    )
                    
                    messages.success(request, f'Successfully added ${profit_amount} profit to {user.username}')
                    return redirect('admin:user_management_usermanagementproxy_changelist')
                    
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
            else:
                messages.error(request, 'Please fill in all required fields')
        
        # Get users for the form
        users = User.objects.filter(is_active=True).order_by('username')
        
        context = {
            'title': 'Add Manual Profit to User',
            'users': users,
        }
        return TemplateResponse(request, 'admin/add_profit.html', context)
    
    def quick_actions_view(self, request):
        if request.method == 'POST':
            action = request.POST.get('action')
            user_id = request.POST.get('user')
            
            if action and user_id:
                try:
                    user = User.objects.get(id=user_id)
                    
                    if action == 'create_portfolio':
                        portfolio, created = UserPortfolio.objects.get_or_create(user=user)
                        if created:
                            messages.success(request, f'Created portfolio for {user.username}')
                        else:
                            messages.info(request, f'Portfolio already exists for {user.username}')
                    
                    elif action == 'reset_portfolio':
                        try:
                            portfolio = UserPortfolio.objects.get(user=user)
                            portfolio.delete()
                            messages.success(request, f'Reset portfolio for {user.username}')
                        except UserPortfolio.DoesNotExist:
                            messages.info(request, f'No portfolio found for {user.username}')
                    
                    return redirect('admin:user_management_usermanagementproxy_changelist')
                    
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
        
        # Get users for the form
        users = User.objects.filter(is_active=True).order_by('username')
        
        context = {
            'title': 'Quick Actions for Users',
            'users': users,
        }
        return TemplateResponse(request, 'admin/quick_actions.html', context)

# Register the proxy model with our custom admin
admin.site.register(UserManagementProxy, UserManagementAdmin) 