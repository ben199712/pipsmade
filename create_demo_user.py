import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from investments.models import InvestmentPlan, UserInvestment, UserPortfolio
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

# Create demo user
username = 'demo'
try:
    user = User.objects.get(username=username)
    print(f'✅ Demo user "{username}" already exists')
except User.DoesNotExist:
    user = User.objects.create_user(
        username=username,
        email='demo@pipsmade.com',
        password='demo123',
        first_name='Demo',
        last_name='User'
    )
    print(f'✅ Created demo user: {username} (password: demo123)')

# Clear existing investments
UserInvestment.objects.filter(user=user).delete()

# Get available plans
plans = list(InvestmentPlan.objects.filter(is_active=True))
print(f'📊 Found {len(plans)} investment plans')

# Create sample investments
sample_investments = [
    {'plan_name': 'Bitcoin Starter', 'amount': 500.00, 'days_ago': 15},
    {'plan_name': 'Blue Chip Stocks', 'amount': 2000.00, 'days_ago': 25},
    {'plan_name': 'Forex Starter', 'amount': 750.00, 'days_ago': 10},
    {'plan_name': 'Growth Stocks', 'amount': 1500.00, 'days_ago': 20},
    {'plan_name': 'Crypto Pro', 'amount': 3000.00, 'days_ago': 5},
]

created_count = 0
for inv_data in sample_investments:
    try:
        plan = InvestmentPlan.objects.get(name=inv_data['plan_name'])
        
        # Generate ROI within plan range
        roi_percentage = Decimal(str(round(random.uniform(
            float(plan.min_roi_percentage), 
            float(plan.max_roi_percentage)
        ), 2)))
        
        # Set start date
        start_date = timezone.now() - timedelta(days=inv_data['days_ago'])
        
        investment = UserInvestment(
            user=user,
            investment_plan=plan,
            amount=Decimal(str(inv_data['amount'])),
            roi_percentage=roi_percentage,
            start_date=start_date,
            status='active'
        )
        
        # Set end date
        investment.end_date = start_date + timedelta(days=plan.duration_days)
        
        # Calculate expected return
        investment.expected_return = investment.amount * (investment.roi_percentage / 100)
        
        # Calculate current value based on progress
        now = timezone.now()
        total_duration = (investment.end_date - investment.start_date).total_seconds()
        elapsed_duration = (now - investment.start_date).total_seconds()
        
        if elapsed_duration <= 0:
            progress = 0
        elif elapsed_duration >= total_duration:
            progress = 1
            investment.status = 'completed'
        else:
            progress = elapsed_duration / total_duration
        
        investment.current_value = investment.amount + (investment.expected_return * Decimal(str(progress)))
        
        investment.save()
        created_count += 1
        
        print(f'✅ Created investment: {plan.name} - ${inv_data["amount"]} ({roi_percentage}% ROI)')
        
    except InvestmentPlan.DoesNotExist:
        print(f'❌ Plan not found: {inv_data["plan_name"]}')
    except Exception as e:
        print(f'❌ Error creating investment: {e}')

# Update portfolio
portfolio = UserPortfolio.get_or_create_portfolio(user)
portfolio.update_portfolio_metrics()

print(f'\n🎉 Successfully created {created_count} sample investments!')
print(f'\n📈 Portfolio Summary for {username}:')
print(f'  💰 Total Invested: ${portfolio.total_invested}')
print(f'  📊 Current Value: ${portfolio.total_current_value}')
print(f'  💵 Total Profit: ${portfolio.total_profit}')
print(f'  📈 ROI: {portfolio.total_roi_percentage}%')
print(f'  🔄 Active: {portfolio.active_investments}')
print(f'  ✅ Completed: {portfolio.completed_investments}')

print(f'\n🚀 You can now login with:')
print(f'   Username: {username}')
print(f'   Password: demo123')
