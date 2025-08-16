from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
import json

@login_required
def dashboard_view(request):
    # Import here to avoid circular imports
    from investments.models import UserPortfolio, UserInvestment, InvestmentReturn
    from transactions.models import Transaction, UserWallet, DepositRequest, WithdrawalRequest
    from django.db.models import Sum, Count, Q
    from django.utils import timezone
    from datetime import timedelta
    import json

    try:
        # Get or create user portfolio
        portfolio = UserPortfolio.get_or_create_portfolio(request.user)

        # Get recent investments
        recent_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')[:5]

        # NO automatic portfolio updates - admin controls everything manually
        # portfolio.update_portfolio_metrics()  # REMOVED - NO AUTOMATIC UPDATES

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
        
        # Calculate total crypto balance in USD (simplified - you might want to add real-time rates)
        total_crypto_balance = sum(wallet.balance for wallet in user_wallets)
        
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
        recent_returns = InvestmentReturn.objects.filter(
            investment__user=request.user,
            date__gte=thirty_days_ago
        ).order_by('date').values('date', 'daily_return')

        # Prepare chart data
        performance_data = []
        if recent_returns:
            cumulative = 0
            for ret in recent_returns:
                cumulative += float(ret['daily_return'])
                performance_data.append({
                    'date': ret['date'].strftime('%Y-%m-%d'),
                    'daily_return': float(ret['daily_return']),
                    'cumulative': cumulative
                })

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
            'total_balance': portfolio.total_withdrawable + total_crypto_balance,  # Total withdrawable + crypto
            'total_profit': portfolio.total_profit,
            'active_investments': portfolio.active_investments,
            'roi_percentage': portfolio.total_roi_percentage,
            'recent_investments': recent_investments,
            'recent_transactions': recent_transactions,
            'pending_deposits': pending_deposits,
            'pending_withdrawals': pending_withdrawals,
            'user_wallets': user_wallets,
            'total_crypto_balance': total_crypto_balance,
            'plan_distribution': plan_distribution,
            'performance_data': json.dumps(performance_data),
            'allocation_data': json.dumps(allocation_data),
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'monthly_change': monthly_change,
            'monthly_change_percentage': monthly_change_percentage,
            'total_withdrawable': portfolio.total_withdrawable,  # NEW: Total withdrawable amount
            'manual_profit_total': portfolio.manual_profit_total,  # NEW: Manual profit total
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
            'performance_data': json.dumps([]),
            'allocation_data': json.dumps([]),
            'total_deposits': 0,
            'total_withdrawals': 0,
            'monthly_change': 0,
            'monthly_change_percentage': 0,
            'total_withdrawable': 0,
        }
        
        return render(request, 'dashboard/dashboard.html', context)

class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Import models
            from investments.models import UserPortfolio, UserInvestment, InvestmentReturn
            from transactions.models import Transaction, UserWallet
            from django.db.models import Sum, Count, Q
            from django.utils import timezone
            from datetime import timedelta
            import json

            # Get user portfolio
            portfolio = UserPortfolio.get_or_create_portfolio(self.request.user)
            # portfolio.update_portfolio_metrics() # REMOVED - NO AUTOMATIC UPDATES

            # Get all user investments
            investments = UserInvestment.objects.filter(user=self.request.user).select_related('investment_plan')
            
            # Get investment plan distribution
            plan_distribution = investments.values('investment_plan__name', 'investment_plan__plan_type', 'admin_investment_plan__name', 'admin_investment_plan__plan_type').annotate(
                total_amount=Sum('amount'),
                count=Count('id'),
                current_value=Sum('current_value')
            ).order_by('-total_amount')
            
            # Process plan distribution to handle both plan types
            processed_plan_distribution = []
            for plan in plan_distribution:
                plan_name = plan['investment_plan__name'] or plan['admin_investment_plan__name']
                plan_type = plan['investment_plan__plan_type'] or plan['admin_investment_plan__plan_type']
                if plan_name:
                    processed_plan_distribution.append({
                        'name': plan_name,
                        'plan_type': plan_type,
                        'total_amount': plan['total_amount'],
                        'count': plan['count'],
                        'current_value': plan['current_value']
                    })
            
            plan_distribution = processed_plan_distribution

            # Get recent returns for performance chart (last 90 days)
            ninety_days_ago = timezone.now().date() - timedelta(days=90)
            recent_returns = InvestmentReturn.objects.filter(
                investment__user=self.request.user,
                date__gte=ninety_days_ago
            ).order_by('date').values('date', 'daily_return')

            # Prepare performance data
            performance_data = []
            if recent_returns:
                cumulative = 0
                for ret in recent_returns:
                    cumulative += float(ret['daily_return'])
                    performance_data.append({
                        'date': ret['date'].strftime('%Y-%m-%d'),
                        'daily_return': float(ret['daily_return']),
                        'cumulative': cumulative
                    })

            # Prepare asset allocation data
            allocation_data = []
            total_portfolio_value = portfolio.total_current_value or 0
            
            if plan_distribution:
                for plan in plan_distribution:
                    if total_portfolio_value > 0:
                        percentage = (float(plan['current_value'] or 0) / total_portfolio_value) * 100
                    else:
                        percentage = 0
                    
                    allocation_data.append({
                        'label': plan['name'],
                        'type': plan['plan_type'],
                        'value': float(plan['current_value'] or 0),
                        'amount': float(plan['total_amount'] or 0),
                        'count': plan['count'],
                        'percentage': percentage
                    })

            # Get user wallets
            user_wallets = UserWallet.objects.filter(user=self.request.user)
            
            # Calculate crypto allocation
            total_crypto_value = sum(wallet.balance for wallet in user_wallets)  # Simplified - should use real rates
            if total_crypto_value > 0 and total_portfolio_value > 0:
                crypto_percentage = (total_crypto_value / total_portfolio_value) * 100
            else:
                crypto_percentage = 0

            # Add crypto to allocation if exists
            if total_crypto_value > 0:
                allocation_data.append({
                    'label': 'Crypto Wallets',
                    'type': 'crypto',
                    'value': total_crypto_value,
                    'amount': total_crypto_value,
                    'count': user_wallets.count(),
                    'percentage': crypto_percentage
                })

            # Get recent transactions
            recent_transactions = Transaction.objects.filter(
                user=self.request.user
            ).order_by('-created_at')[:10]

            # Calculate performance metrics
            if recent_returns:
                returns_list = [float(r['daily_return']) for r in recent_returns]
                avg_return = sum(returns_list) / len(returns_list)
                max_return = max(returns_list)
                min_return = min(returns_list)
                
                # Simple volatility calculation
                variance = sum((r - avg_return) ** 2 for r in returns_list) / len(returns_list)
                volatility = (variance ** 0.5) * 100
                
                # Max drawdown simulation
                max_drawdown = 0
                peak = 0
                for ret in returns_list:
                    if ret > peak:
                        peak = ret
                    drawdown = (peak - ret) / peak * 100 if peak > 0 else 0
                    if drawdown > max_drawdown:
                        max_drawdown = drawdown
            else:
                avg_return = 0
                max_return = 0
                min_return = 0
                volatility = 0
                max_drawdown = 0

            # Calculate today's change
            today = timezone.now().date()
            today_return = InvestmentReturn.objects.filter(
                investment__user=self.request.user,
                date=today
            ).aggregate(total=Sum('daily_return'))['total'] or 0

            context.update({
                'portfolio': portfolio,
                'investments': investments,
                'plan_distribution': plan_distribution,
                'performance_data': json.dumps(performance_data),
                'allocation_data': json.dumps(allocation_data),
                'recent_transactions': recent_transactions,
                'user_wallets': user_wallets,
                'total_crypto_value': total_crypto_value,
                'today_return': today_return,
                'avg_return': avg_return,
                'max_return': max_return,
                'min_return': min_return,
                'volatility': volatility,
                'max_drawdown': max_drawdown,
                'total_portfolio_value': total_portfolio_value,
            })
            
        except Exception as e:
            print(f"Portfolio error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Provide safe defaults
            context.update({
                'portfolio': None,
                'investments': [],
                'plan_distribution': [],
                'performance_data': json.dumps([]),
                'allocation_data': json.dumps([]),
                'recent_transactions': [],
                'user_wallets': [],
                'total_crypto_value': 0,
                'today_return': 0,
                'avg_return': 0,
                'max_return': 0,
                'min_return': 0,
                'volatility': 0,
                'max_drawdown': 0,
                'total_portfolio_value': 0,
            })

        context['page_title'] = 'Portfolio'
        return context

class DepositView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/deposit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Deposit Funds'
        return context

class WithdrawView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/withdraw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Withdraw Funds'
        return context
