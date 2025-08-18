from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
import random
from .models import InvestmentPlan, UserInvestment, UserPortfolio
from transactions.models import TransactionNotification
from .forms import InvestmentForm

@login_required
def investments_view(request):
    """Display available investment plans and user's investments"""
    investment_plans = InvestmentPlan.objects.filter(is_active=True)
    user_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')

    # Update current values for active investments
    for investment in user_investments.filter(status='active'):
        investment.update_current_value()
        investment.save()

    # Get or create user portfolio
    portfolio = UserPortfolio.get_or_create_portfolio(request.user)

    context = {
        'investment_plans': investment_plans,
        'user_investments': user_investments,
        'portfolio': portfolio,
        'active_investments': user_investments.filter(status='active'),
        'completed_investments': user_investments.filter(status='completed'),
        'unread_notifications': TransactionNotification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')[:10],
    }

    return render(request, 'dashboard/investments.html', context)

@login_required
def create_investment(request):
    """Create a new investment"""
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        amount = request.POST.get('amount')

        try:
            plan = get_object_or_404(InvestmentPlan, id=plan_id, is_active=True)
            amount = Decimal(str(amount))

            # Validate investment amount
            if amount < plan.min_investment:
                messages.error(request, f'Minimum investment for {plan.name} is ${plan.min_investment}')
                return redirect('investments')

            if plan.max_investment and amount > plan.max_investment:
                messages.error(request, f'Maximum investment for {plan.name} is ${plan.max_investment}')
                return redirect('investments')

            # Generate ROI percentage within plan range
            roi_percentage = Decimal(str(random.uniform(
                float(plan.min_roi_percentage),
                float(plan.max_roi_percentage)
            )))
            roi_percentage = round(roi_percentage, 2)

            # Create investment
            investment = UserInvestment.objects.create(
                user=request.user,
                investment_plan=plan,
                amount=amount,
                roi_percentage=roi_percentage
            )

            # Send admin notification
            try:
                send_mail(
                    subject='New Investment Created',
                    message=f'User {request.user.get_full_name() or request.user.username} created a new investment:\n'
                           f'Plan: {plan.name}\n'
                           f'Amount: ${amount}\n'
                           f'ROI: {roi_percentage}%\n'
                           f'Duration: {plan.duration_days} days',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except:
                pass

            # Update user portfolio
            portfolio = UserPortfolio.get_or_create_portfolio(request.user)
            portfolio.update_portfolio_metrics()

            messages.success(request, f'Investment of ${amount} in {plan.name} created successfully!')
            return redirect('investments')

        except (ValueError, TypeError):
            messages.error(request, 'Invalid investment amount')
        except Exception as e:
            messages.error(request, 'An error occurred while creating your investment')

    return redirect('investments')

@login_required
def investment_detail(request, investment_id):
    """View detailed information about a specific investment"""
    investment = get_object_or_404(UserInvestment, id=investment_id, user=request.user)

    # Update current value
    investment.update_current_value()
    investment.save()

    # Get investment returns history
    returns = investment.returns.all()[:30]  # Last 30 days

    context = {
        'investment': investment,
        'returns': returns,
        'progress_percentage': investment.get_progress_percentage(),
        'days_remaining': investment.days_remaining(),
        'current_profit': investment.get_profit(),
    }

    return render(request, 'dashboard/investment_detail.html', context)

@login_required
def cancel_investment(request, investment_id):
    """Cancel an active investment"""
    if request.method == 'POST':
        investment = get_object_or_404(UserInvestment, id=investment_id, user=request.user)

        if investment.status == 'active':
            investment.status = 'cancelled'
            investment.save()

            # Update portfolio
            portfolio = UserPortfolio.get_or_create_portfolio(request.user)
            portfolio.update_portfolio_metrics()

            messages.success(request, f'Investment in {investment.investment_plan.name} has been cancelled')
        else:
            messages.error(request, 'Only active investments can be cancelled')

    return redirect('investments')

@login_required
def investment_calculator(request):
    """AJAX endpoint for investment calculator"""
    if request.method == 'GET':
        plan_id = request.GET.get('plan_id')
        amount = request.GET.get('amount')

        try:
            plan = get_object_or_404(InvestmentPlan, id=plan_id)
            amount = Decimal(str(amount))

            # Calculate potential returns
            min_return = amount * (plan.min_roi_percentage / 100)
            max_return = amount * (plan.max_roi_percentage / 100)
            avg_return = amount * (plan.get_average_roi() / 100)

            data = {
                'min_return': float(min_return),
                'max_return': float(max_return),
                'avg_return': float(avg_return),
                'min_total': float(amount + min_return),
                'max_total': float(amount + max_return),
                'avg_total': float(amount + avg_return),
                'duration_days': plan.duration_days,
                'plan_name': plan.name,
            }

            return JsonResponse(data)

        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Calculation error'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
