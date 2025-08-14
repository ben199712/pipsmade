from django.core.management.base import BaseCommand
from investments.models import InvestmentPlan

class Command(BaseCommand):
    help = 'Create sample investment plans'

    def handle(self, *args, **options):
        # Clear existing plans
        InvestmentPlan.objects.all().delete()
        
        # Cryptocurrency Plans
        crypto_plans = [
            {
                'name': 'Bitcoin Starter',
                'plan_type': 'crypto',
                'description': 'Entry-level Bitcoin investment plan with moderate returns. Perfect for beginners looking to enter the cryptocurrency market.',
                'min_investment': 100.00,
                'max_investment': 5000.00,
                'min_roi_percentage': 15.0,
                'max_roi_percentage': 25.0,
                'duration_days': 30,
                'risk_level': 'high',
                'features': [
                    'Bitcoin portfolio management',
                    'Daily market analysis',
                    'Risk management tools',
                    '24/7 monitoring'
                ]
            },
            {
                'name': 'Crypto Pro',
                'plan_type': 'crypto',
                'description': 'Advanced cryptocurrency trading with diversified altcoin portfolio. Higher returns with professional management.',
                'min_investment': 1000.00,
                'max_investment': 25000.00,
                'min_roi_percentage': 20.0,
                'max_roi_percentage': 35.0,
                'duration_days': 60,
                'risk_level': 'high',
                'features': [
                    'Multi-coin portfolio',
                    'Advanced trading strategies',
                    'DeFi opportunities',
                    'Expert analysis',
                    'Priority support'
                ]
            },
            {
                'name': 'Crypto Elite',
                'plan_type': 'crypto',
                'description': 'Premium cryptocurrency investment with access to exclusive opportunities and maximum returns.',
                'min_investment': 5000.00,
                'max_investment': 100000.00,
                'min_roi_percentage': 25.0,
                'max_roi_percentage': 45.0,
                'duration_days': 90,
                'risk_level': 'high',
                'features': [
                    'Exclusive crypto opportunities',
                    'Institutional-grade strategies',
                    'Private blockchain investments',
                    'Dedicated account manager',
                    'VIP support'
                ]
            }
        ]
        
        # Stock Market Plans
        stock_plans = [
            {
                'name': 'Blue Chip Stocks',
                'plan_type': 'stocks',
                'description': 'Conservative stock investment focusing on established companies with steady growth and dividend income.',
                'min_investment': 500.00,
                'max_investment': 50000.00,
                'min_roi_percentage': 8.0,
                'max_roi_percentage': 15.0,
                'duration_days': 90,
                'risk_level': 'low',
                'features': [
                    'Fortune 500 companies',
                    'Dividend-paying stocks',
                    'Quarterly rebalancing',
                    'Risk-adjusted returns'
                ]
            },
            {
                'name': 'Growth Stocks',
                'plan_type': 'stocks',
                'description': 'High-growth potential stocks from emerging sectors including technology, healthcare, and renewable energy.',
                'min_investment': 1000.00,
                'max_investment': 75000.00,
                'min_roi_percentage': 12.0,
                'max_roi_percentage': 22.0,
                'duration_days': 120,
                'risk_level': 'medium',
                'features': [
                    'High-growth companies',
                    'Sector diversification',
                    'Growth-focused strategy',
                    'Monthly performance reports'
                ]
            },
            {
                'name': 'Tech Innovation',
                'plan_type': 'stocks',
                'description': 'Cutting-edge technology stocks including AI, robotics, and next-generation companies.',
                'min_investment': 2000.00,
                'max_investment': 100000.00,
                'min_roi_percentage': 15.0,
                'max_roi_percentage': 30.0,
                'duration_days': 180,
                'risk_level': 'high',
                'features': [
                    'AI and robotics stocks',
                    'Emerging tech companies',
                    'Innovation-focused portfolio',
                    'Expert tech analysis'
                ]
            }
        ]
        
        # Forex Trading Plans
        forex_plans = [
            {
                'name': 'Forex Starter',
                'plan_type': 'forex',
                'description': 'Conservative forex trading focusing on major currency pairs with professional risk management.',
                'min_investment': 250.00,
                'max_investment': 10000.00,
                'min_roi_percentage': 10.0,
                'max_roi_percentage': 18.0,
                'duration_days': 45,
                'risk_level': 'medium',
                'features': [
                    'Major currency pairs',
                    'Professional traders',
                    'Risk management',
                    'Daily market updates'
                ]
            },
            {
                'name': 'Forex Pro',
                'plan_type': 'forex',
                'description': 'Advanced forex strategies including exotic pairs and algorithmic trading for higher returns.',
                'min_investment': 1000.00,
                'max_investment': 50000.00,
                'min_roi_percentage': 15.0,
                'max_roi_percentage': 25.0,
                'duration_days': 75,
                'risk_level': 'medium',
                'features': [
                    'Exotic currency pairs',
                    'Algorithmic trading',
                    'Advanced strategies',
                    'Real-time signals'
                ]
            }
        ]
        
        # Bonds & Fixed Income Plans
        bond_plans = [
            {
                'name': 'Government Bonds',
                'plan_type': 'bonds',
                'description': 'Safe and stable government bond investments with guaranteed returns and capital protection.',
                'min_investment': 1000.00,
                'max_investment': 200000.00,
                'min_roi_percentage': 5.0,
                'max_roi_percentage': 8.0,
                'duration_days': 180,
                'risk_level': 'low',
                'features': [
                    'Government-backed securities',
                    'Capital protection',
                    'Stable returns',
                    'Low volatility'
                ]
            },
            {
                'name': 'Corporate Bonds',
                'plan_type': 'bonds',
                'description': 'Higher-yield corporate bonds from investment-grade companies with attractive fixed returns.',
                'min_investment': 2000.00,
                'max_investment': 150000.00,
                'min_roi_percentage': 7.0,
                'max_roi_percentage': 12.0,
                'duration_days': 365,
                'risk_level': 'low',
                'features': [
                    'Investment-grade bonds',
                    'Fixed interest payments',
                    'Diversified portfolio',
                    'Credit risk management'
                ]
            },
            {
                'name': 'High-Yield Bonds',
                'plan_type': 'bonds',
                'description': 'Premium bond portfolio with higher yields from carefully selected corporate and municipal bonds.',
                'min_investment': 5000.00,
                'max_investment': 300000.00,
                'min_roi_percentage': 10.0,
                'max_roi_percentage': 15.0,
                'duration_days': 540,
                'risk_level': 'medium',
                'features': [
                    'High-yield opportunities',
                    'Municipal bonds',
                    'Enhanced returns',
                    'Professional management'
                ]
            }
        ]
        
        # Create all plans
        all_plans = crypto_plans + stock_plans + forex_plans + bond_plans
        
        created_count = 0
        for plan_data in all_plans:
            plan, created = InvestmentPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan already exists: {plan.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} investment plans!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total plans in database: {InvestmentPlan.objects.count()}')
        )
