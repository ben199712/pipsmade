import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from investments.models import InvestmentPlan

# Clear existing plans
InvestmentPlan.objects.all().delete()

# Create sample plans
plans_data = [
    # Cryptocurrency Plans
    {
        'name': 'Bitcoin Starter',
        'plan_type': 'crypto',
        'description': 'Entry-level Bitcoin investment plan with moderate returns.',
        'min_investment': 100.00,
        'max_investment': 5000.00,
        'min_roi_percentage': 15.0,
        'max_roi_percentage': 25.0,
        'duration_days': 30,
        'risk_level': 'high',
        'features': ['Bitcoin portfolio', 'Daily analysis', 'Risk management', '24/7 monitoring']
    },
    {
        'name': 'Crypto Pro',
        'plan_type': 'crypto',
        'description': 'Advanced cryptocurrency trading with diversified portfolio.',
        'min_investment': 1000.00,
        'max_investment': 25000.00,
        'min_roi_percentage': 20.0,
        'max_roi_percentage': 35.0,
        'duration_days': 60,
        'risk_level': 'high',
        'features': ['Multi-coin portfolio', 'Advanced strategies', 'DeFi opportunities']
    },
    
    # Stock Plans
    {
        'name': 'Blue Chip Stocks',
        'plan_type': 'stocks',
        'description': 'Conservative stock investment in established companies.',
        'min_investment': 500.00,
        'max_investment': 50000.00,
        'min_roi_percentage': 8.0,
        'max_roi_percentage': 15.0,
        'duration_days': 90,
        'risk_level': 'low',
        'features': ['Fortune 500 companies', 'Dividend stocks', 'Quarterly rebalancing']
    },
    {
        'name': 'Growth Stocks',
        'plan_type': 'stocks',
        'description': 'High-growth potential stocks from emerging sectors.',
        'min_investment': 1000.00,
        'max_investment': 75000.00,
        'min_roi_percentage': 12.0,
        'max_roi_percentage': 22.0,
        'duration_days': 120,
        'risk_level': 'medium',
        'features': ['High-growth companies', 'Sector diversification', 'Growth strategy']
    },
    
    # Forex Plans
    {
        'name': 'Forex Starter',
        'plan_type': 'forex',
        'description': 'Conservative forex trading with major currency pairs.',
        'min_investment': 250.00,
        'max_investment': 10000.00,
        'min_roi_percentage': 10.0,
        'max_roi_percentage': 18.0,
        'duration_days': 45,
        'risk_level': 'medium',
        'features': ['Major currency pairs', 'Professional traders', 'Risk management']
    },
    
    # Bonds Plans
    {
        'name': 'Government Bonds',
        'plan_type': 'bonds',
        'description': 'Safe government bond investments with guaranteed returns.',
        'min_investment': 1000.00,
        'max_investment': 200000.00,
        'min_roi_percentage': 5.0,
        'max_roi_percentage': 8.0,
        'duration_days': 180,
        'risk_level': 'low',
        'features': ['Government-backed', 'Capital protection', 'Stable returns']
    },
]

# Create the plans
created_count = 0
for plan_data in plans_data:
    plan, created = InvestmentPlan.objects.get_or_create(
        name=plan_data['name'],
        defaults=plan_data
    )
    if created:
        created_count += 1
        print(f'✅ Created: {plan.name}')
    else:
        print(f'⚠️  Already exists: {plan.name}')

print(f'\n🎉 Successfully created {created_count} investment plans!')
print(f'📊 Total plans in database: {InvestmentPlan.objects.count()}')

# Display all plans
print('\n📋 Available Investment Plans:')
for plan in InvestmentPlan.objects.all():
    print(f'  • {plan.name} ({plan.get_plan_type_display()})')
    print(f'    ROI: {plan.min_roi_percentage}% - {plan.max_roi_percentage}%')
    print(f'    Min: ${plan.min_investment}, Duration: {plan.duration_days} days')
    print(f'    Risk: {plan.get_risk_level_display()}')
    print()
