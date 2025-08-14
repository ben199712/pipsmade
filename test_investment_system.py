import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from investments.models import InvestmentPlan, UserInvestment, UserPortfolio

def test_investment_system():
    print("🧪 Testing Investment System...")
    
    # Test 1: Check investment plans
    plans = InvestmentPlan.objects.all()
    print(f"\n📊 Investment Plans: {plans.count()} found")
    for plan in plans:
        print(f"  • {plan.name}: {plan.min_roi_percentage}%-{plan.max_roi_percentage}% ROI")
    
    # Test 2: Check demo user
    try:
        demo_user = User.objects.get(username='demo')
        print(f"\n👤 Demo User: {demo_user.username} ({demo_user.email})")
        
        # Test 3: Check user investments
        investments = UserInvestment.objects.filter(user=demo_user)
        print(f"\n💰 User Investments: {investments.count()} found")
        for inv in investments:
            print(f"  • {inv.investment_plan.name}: ${inv.amount} -> ${inv.current_value} ({inv.status})")
        
        # Test 4: Check portfolio
        portfolio = UserPortfolio.objects.filter(user=demo_user).first()
        if portfolio:
            print(f"\n📈 Portfolio Summary:")
            print(f"  Total Invested: ${portfolio.total_invested}")
            print(f"  Current Value: ${portfolio.total_current_value}")
            print(f"  Total Profit: ${portfolio.total_profit}")
            print(f"  ROI: {portfolio.total_roi_percentage:.2f}%")
            print(f"  Active: {portfolio.active_investments}, Completed: {portfolio.completed_investments}")
        
    except User.DoesNotExist:
        print("❌ Demo user not found. Run create_demo_user.py first.")
    
    # Test 5: Test ROI calculations
    if plans.exists():
        test_plan = plans.first()
        test_amount = 1000
        potential_return = test_plan.calculate_potential_return(test_amount)
        print(f"\n🧮 ROI Calculation Test:")
        print(f"  Plan: {test_plan.name}")
        print(f"  Investment: ${test_amount}")
        print(f"  Potential Return: ${potential_return}")
        print(f"  Total Payout: ${test_amount + potential_return}")
    
    print(f"\n✅ Investment System Test Complete!")
    print(f"\n🚀 Ready to use! Start server with: python manage.py runserver")
    print(f"   Then visit: http://127.0.0.1:8000/investments/")

if __name__ == '__main__':
    test_investment_system()
