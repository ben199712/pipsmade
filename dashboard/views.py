from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

@login_required
def dashboard_view(request):
    # Import here to avoid circular imports
    from investments.models import UserPortfolio, UserInvestment

    # Get or create user portfolio
    portfolio = UserPortfolio.get_or_create_portfolio(request.user)

    # Get recent investments
    recent_investments = UserInvestment.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Update portfolio metrics
    portfolio.update_portfolio_metrics()

    context = {
        'user': request.user,
        'portfolio': portfolio,
        'total_balance': portfolio.total_current_value,
        'total_profit': portfolio.total_profit,
        'active_investments': portfolio.active_investments,
        'roi_percentage': portfolio.total_roi_percentage,
        'recent_investments': recent_investments,
    }
    return render(request, 'dashboard/dashboard.html', context)

class PortfolioView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
