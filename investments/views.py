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

    # NO automatic updates - admin controls everything manually
    # for investment in user_investments.filter(status='active'):
    #     investment.update_current_value()
    #     investment.save()

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
    print("=" * 50)
    print("DEBUG: create_investment view called!")
    print(f"DEBUG: Method: {request.method}")
    print(f"DEBUG: User: {request.user.username}")
    print(f"DEBUG: Request headers: {dict(request.headers)}")
    print("=" * 50)
    
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        amount = request.POST.get('amount')
        
        print(f"DEBUG: Received plan_id: {plan_id}, amount: {amount}")
        print(f"DEBUG: All POST data: {dict(request.POST)}")
        print(f"DEBUG: Content type: {request.content_type}")
        print(f"DEBUG: Is AJAX request: {request.headers.get('X-Requested-With') == 'XMLHttpRequest'}")

        # Validate required fields
        if not plan_id:
            error_msg = 'Investment plan is required'
            print(f"DEBUG: Missing plan_id: {error_msg}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect('investments')

        if not amount:
            error_msg = 'Investment amount is required'
            print(f"DEBUG: Missing amount: {error_msg}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
            return redirect('investments')

        try:
            plan = get_object_or_404(InvestmentPlan, id=plan_id, is_active=True)
            print(f"DEBUG: Found plan: {plan.name}")
            
            amount = Decimal(str(amount))
            print(f"DEBUG: Converted amount to Decimal: {amount}")

            # Validate investment amount
            if amount < plan.min_investment:
                print(f"DEBUG: Amount {amount} is less than minimum {plan.min_investment}")
                error_msg = f'Minimum investment for {plan.name} is ${plan.min_investment}'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_msg})
                messages.error(request, error_msg)
                return redirect('investments')

            if plan.max_investment and amount > plan.max_investment:
                print(f"DEBUG: Amount {amount} is greater than maximum {plan.max_investment}")
                error_msg = f'Maximum investment for {plan.name} is ${plan.max_investment}'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_msg})
                messages.error(request, error_msg)
                return redirect('investments')

            # Generate ROI percentage within plan range
            roi_percentage = Decimal(str(random.uniform(
                float(plan.min_roi_percentage),
                float(plan.max_roi_percentage)
            )))
            roi_percentage = round(roi_percentage, 2)
            print(f"DEBUG: Generated ROI: {roi_percentage}%")

            # Create investment
            print(f"DEBUG: About to create UserInvestment...")
            
            # Calculate expected return based on ROI
            expected_return = amount * (roi_percentage / 100)
            print(f"DEBUG: Calculated expected_return: ${expected_return}")
            
            # Prepare all required fields
            investment_data = {
                'user': request.user,
                'investment_plan': plan,
                'amount': amount,
                'roi_percentage': roi_percentage,
                'expected_return': expected_return,
                'current_value': amount,  # Start with initial amount
                'total_profit': Decimal('0'),  # Start with 0 profit
                'total_withdrawable': amount,  # Start with initial amount as withdrawable
                'manual_profit': Decimal('0'),  # Start with 0 manual profit
            }
            
            print(f"DEBUG: Investment data to create: {investment_data}")
            
            investment = UserInvestment.objects.create(**investment_data)
            print(f"DEBUG: Investment created successfully with ID: {investment.id}")

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
                print(f"DEBUG: Admin notification email sent")
            except Exception as email_error:
                print(f"DEBUG: Email notification failed: {email_error}")
                pass

            # NO automatic portfolio updates - admin controls everything manually
            # portfolio = UserPortfolio.get_or_create_portfolio(request.user)
            # portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES

            success_msg = f'Investment of ${amount} in {plan.name} created successfully!'
            print(f"DEBUG: Success message: {success_msg}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': success_msg,
                    'investment_id': investment.id
                })
            
            messages.success(request, success_msg)
            print(f"DEBUG: Success message added, redirecting to investments")
            return redirect('investments')

        except (ValueError, TypeError) as e:
            print(f"DEBUG: Investment creation error (ValueError/TypeError): {e}")
            error_msg = 'Invalid investment amount'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)
        except Exception as e:
            print(f"DEBUG: Investment creation error: {e}")
            import traceback
            traceback.print_exc()
            error_msg = f'An error occurred while creating your investment: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            messages.error(request, error_msg)

    print(f"DEBUG: Redirecting to investments (GET request or error occurred)")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    return redirect('investments')

@login_required
def investment_detail(request, investment_id):
    """View detailed information about a specific investment"""
    investment = get_object_or_404(UserInvestment, id=investment_id, user=request.user)

    # NO automatic updates - admin controls everything manually
    # investment.update_current_value()

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
