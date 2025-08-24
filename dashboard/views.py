from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import json

# Import models
from transactions.models import UserWallet, Transaction, WithdrawalRequest, DepositRequest, TransactionNotification
from investments.models import UserInvestment, UserPortfolio, InvestmentReturn

# Import forms
from transactions.forms import WithdrawalForm

@login_required
def dashboard_view(request):
    try:
        # Get or create user portfolio
        portfolio = UserPortfolio.get_or_create_portfolio(request.user)
        
        if portfolio:
            pass
        else:
            pass
        
        # Get recent investments
        recent_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')[:5]
        
        # Get recent transactions (last 10)
        recent_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]
        
        # NO automatic portfolio updates - admin controls everything manually
        # portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES

        # Get recent investments
        recent_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')[:5]

        # Get recent transactions (last 10)
        recent_transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-created_at')[:10]

        # Get pending deposits (not yet approved)
        pending_deposits = DepositRequest.objects.filter(
            user=request.user,
            admin_verified=False
        ).order_by('-created_at')[:5]

        # Get pending withdrawals (not yet processed)
        pending_withdrawals = WithdrawalRequest.objects.filter(
            user=request.user,
            transaction__status='pending'
        ).order_by('-created_at')[:5]

        # Get user wallets for asset allocation
        user_wallets = UserWallet.objects.filter(user=request.user)
        
        # Get user notifications
        from transactions.models import TransactionNotification
        unread_notifications = TransactionNotification.objects.filter(
            user=request.user,
            is_read=False
        ).order_by('-created_at')[:10]
        
        recent_notifications = TransactionNotification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        
        # Calculate total crypto balance in USD (simplified - you might want to add real-time rates)
        total_crypto_balance = sum(wallet.balance for wallet in user_wallets)
        
        # Convert to Decimal to avoid type mismatch with portfolio values
        total_crypto_balance = Decimal(str(total_crypto_balance))
        
        # Get investment plan distribution
        plan_distribution = UserInvestment.objects.filter(
            user=request.user, 
            status='active'
        ).values('investment_plan__name', 'admin_investment_plan__name').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        # Process plan distribution to handle both plan types
        processed_plan_distribution = []
        for plan in plan_distribution:
            plan_name = plan['investment_plan__name'] or plan['admin_investment_plan__name']
            if plan_name:
                processed_plan_distribution.append({
                    'name': plan_name,
                    'total_amount': plan['total_amount'],
                    'count': plan['count']
                })
        
        plan_distribution = processed_plan_distribution

        # Get recent returns for performance chart (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        
        # Get investment returns
        recent_returns = InvestmentReturn.objects.filter(
            investment__user=request.user,
            date__gte=thirty_days_ago
        ).order_by('date').values('date', 'daily_return')
        
        # Get manual profits and other manual entries
        manual_entries = []
        
        # Get manual profits from portfolio (if they have dates)
        if hasattr(portfolio, 'manual_profit_total') and portfolio.manual_profit_total:
            # Distribute manual profit over the last 30 days to show growth
            manual_profit_per_day = portfolio.manual_profit_total / 30
            for i in range(30):
                entry_date = timezone.now().date() - timedelta(days=29-i)
                manual_entries.append({
                    'date': entry_date,
                    'amount': manual_profit_per_day
                })
        
        # Get deposits and withdrawals for the period
        recent_transactions_for_chart = Transaction.objects.filter(
            user=request.user,
            created_at__date__gte=thirty_days_ago,
            status='completed'
        ).order_by('created_at').values('created_at', 'transaction_type', 'usd_equivalent', 'amount')
        
        # Asset allocation data for pie chart
        allocation_data = []
        if plan_distribution:
            for plan in plan_distribution:
                allocation_data.append({
                    'label': plan['name'],
                    'value': float(plan['total_amount']),
                    'count': plan['count']
                })

        # Get quick stats
        total_deposits = Transaction.objects.filter(
            user=request.user, 
            transaction_type='deposit', 
            status='completed'
        ).aggregate(total=Sum('usd_equivalent'))['total'] or 0

        total_withdrawals = Transaction.objects.filter(
            user=request.user, 
            transaction_type='withdrawal', 
            status='completed'
        ).aggregate(total=Sum('usd_equivalent'))['total'] or 0

        # Calculate monthly change
        last_month = timezone.now() - timedelta(days=30)
        last_month_portfolio = UserPortfolio.objects.filter(
            user=request.user,
            last_updated__gte=last_month
        ).first()
        
        monthly_change = 0
        monthly_change_percentage = 0
        if last_month_portfolio:
            monthly_change = portfolio.total_current_value - last_month_portfolio.total_current_value
        
        # Safe calculation of monthly change percentage
        if portfolio.total_invested and portfolio.total_invested > 0:
            monthly_change_percentage = (monthly_change / portfolio.total_invested) * 100

        context = {
            'user': request.user,
            'portfolio': portfolio,
            'total_balance': (portfolio.total_withdrawable + total_crypto_balance) if portfolio else total_crypto_balance,
            'total_profit': portfolio.total_profit if portfolio else Decimal('0'),
            'active_investments': portfolio.active_investments if portfolio else 0,
            'roi_percentage': portfolio.total_roi_percentage if portfolio else Decimal('0'),
            'recent_investments': recent_investments,
            'recent_transactions': recent_transactions,
            'pending_deposits': pending_deposits,
            'pending_withdrawals': pending_withdrawals,
            'user_wallets': user_wallets,
            'total_crypto_balance': total_crypto_balance,
            'plan_distribution': plan_distribution,
            'allocation_data': json.dumps(allocation_data),
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'monthly_change': monthly_change,
            'monthly_change_percentage': monthly_change_percentage,
            'total_withdrawable': portfolio.total_withdrawable if portfolio else Decimal('0'),
            'manual_profit_total': portfolio.manual_profit_total if portfolio else Decimal('0'),
            'unread_notifications': unread_notifications,
            'recent_notifications': recent_notifications,
        }
        
        return render(request, 'dashboard/dashboard.html', context)
        
    except Exception as e:
        # Log the error for debugging
        print(f"Dashboard error: {str(e)}")
        
        # Return a basic context with error handling
        context = {
            'user': request.user,
            'portfolio': None,
            'total_balance': 0,
            'total_profit': 0,
            'active_investments': 0,
            'roi_percentage': 0,
            'recent_investments': [],
            'recent_transactions': [],
            'pending_deposits': [],
            'pending_withdrawals': [],
            'user_wallets': [],
            'total_crypto_balance': 0,
            'plan_distribution': [],
            'allocation_data': json.dumps([]),
            'total_deposits': 0,
            'total_withdrawals': 0,
            'monthly_change': 0,
            'monthly_change_percentage': 0,
            'total_withdrawable': 0,
            'unread_notifications': [],
            'recent_notifications': [],
        }
        
        return render(request, 'dashboard/dashboard.html', context)

class DepositView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/deposit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Get user notifications
            from transactions.models import TransactionNotification
            unread_notifications = TransactionNotification.objects.filter(
                user=self.request.user,
                is_read=False
            ).order_by('-created_at')[:10]
            
            context['unread_notifications'] = unread_notifications
        except Exception as e:
            print(f"DepositView notification error: {str(e)}")
            context['unread_notifications'] = []
        
        context['page_title'] = 'Deposit Funds'
        return context

class WithdrawView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/withdraw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Get user's wallet balances
            user_wallets = UserWallet.objects.filter(user=self.request.user)
            
            # Calculate crypto balance
            total_crypto_balance = sum(wallet.balance for wallet in user_wallets)
            
            # Get portfolio data
            try:
                portfolio = UserPortfolio.objects.get(user=self.request.user)
                total_portfolio_value = portfolio.total_current_value or 0
            except UserPortfolio.DoesNotExist:
                total_portfolio_value = 0
            
            # Calculate total available balance
            total_available_balance = total_crypto_balance + total_portfolio_value
            
            # Get withdrawal statistics
            total_withdrawals = Transaction.objects.filter(
                user=self.request.user,
                transaction_type='withdrawal',
                status='completed'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            pending_withdrawals = Transaction.objects.filter(
                user=self.request.user,
                transaction_type='withdrawal',
                status='pending'
            ).count()
            
            recent_withdrawals = Transaction.objects.filter(
                user=self.request.user,
                transaction_type='withdrawal'
            ).order_by('-created_at')[:5]
            
            # Create and initialize the withdrawal form
            form = WithdrawalForm(user=self.request.user)
            
            context.update({
                'user_wallets': user_wallets,
                'total_crypto_balance': total_crypto_balance,
                'total_portfolio_value': total_portfolio_value,
                'total_available_balance': total_available_balance,
                'total_withdrawals': total_withdrawals,
                'pending_withdrawals': pending_withdrawals,
                'recent_withdrawals': recent_withdrawals,
                'form': form,  # Now properly providing the form
            })
            
        except Exception as e:
            print(f"WithdrawView error: {str(e)}")
            # Provide safe defaults
            context.update({
                'user_wallets': [],
                'total_crypto_balance': 0,
                'total_portfolio_value': 0,
                'total_available_balance': 0,
                'total_withdrawals': 0,
                'pending_withdrawals': 0,
                'recent_withdrawals': [],
                'form': WithdrawalForm(user=self.request.user),  # Provide form even on error
            })
        
        context['page_title'] = 'Withdraw Funds'
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission"""
        form = WithdrawalForm(request.POST, user=request.user)
        
        if form.is_valid():
            try:
                crypto_type = form.cleaned_data['crypto_type']
                amount = form.cleaned_data['amount']
                destination_address = form.cleaned_data['destination_address']
                network = form.cleaned_data['network']

                # Get user's wallet balance
                try:
                    user_wallet = UserWallet.objects.get(user=request.user, crypto_type=crypto_type)
                except UserWallet.DoesNotExist:
                    messages.error(request, f'You do not have a {crypto_type} wallet.')
                    return self.get(request, *args, **kwargs)

                # Check if user has sufficient balance
                if user_wallet.balance < amount:
                    messages.error(request, f'Insufficient {crypto_type} balance. Available: {user_wallet.balance}')
                    return self.get(request, *args, **kwargs)

                # Calculate fees (default 2% if no specific wallet found)
                platform_fee = amount * Decimal('0.02')  # 2% default fee

                # Create transaction
                transaction = Transaction.objects.create(
                    user=request.user,
                    transaction_type='withdrawal',
                    status='pending',
                    amount=amount,
                    crypto_type=crypto_type,
                    to_address=destination_address,
                    platform_fee=platform_fee,
                    user_notes=f"Withdrawal via {network}"
                )

                # Create withdrawal request
                withdrawal_request = WithdrawalRequest.objects.create(
                    user=request.user,
                    transaction=transaction,
                    crypto_type=crypto_type,
                    amount=amount,
                    destination_address=destination_address,
                    network=network,
                    platform_fee=platform_fee,
                    ip_address=request.META.get('REMOTE_ADDR', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                messages.success(request, 'Withdrawal request submitted successfully! It will be processed by our team.')
                return redirect('transactions')
                
            except Exception as e:
                print(f"Withdrawal creation error: {e}")
                messages.error(request, 'An error occurred while processing your withdrawal request. Please try again.')
        else:
            # Form is invalid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        
        # If we get here, there was an error or invalid form
        # Re-render the page with the form and errors
        return self.get(request, *args, **kwargs)
