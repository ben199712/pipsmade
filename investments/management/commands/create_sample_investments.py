from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from investments.models import InvestmentPlan, UserInvestment, UserPortfolio
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create sample user investments for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to create investments for',
            default='testuser'
        )
        parser.add_argument(
            '--count',
            type=int,
            help='Number of investments to create',
            default=5
        )

    def handle(self, *args, **options):
        username = options['username']
        count = options['count']
        
        # Get or create test user
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Found user: {username}')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created test user: {username}')
            )
        
        # Get available investment plans
        plans = list(InvestmentPlan.objects.filter(is_active=True))
        if not plans:
            self.stdout.write(
                self.style.ERROR('No investment plans found. Run create_sample_plans first.')
            )
            return
        
        # Clear existing investments for this user
        UserInvestment.objects.filter(user=user).delete()
        
        created_count = 0
        for i in range(count):
            # Select random plan
            plan = random.choice(plans)
            
            # Generate random investment amount within plan limits
            min_amount = float(plan.min_investment)
            max_amount = float(plan.max_investment) if plan.max_investment else min_amount * 10
            amount = Decimal(str(round(random.uniform(min_amount, min(max_amount, min_amount * 5)), 2)))
            
            # Generate ROI within plan range
            roi_percentage = Decimal(str(round(random.uniform(
                float(plan.min_roi_percentage), 
                float(plan.max_roi_percentage)
            ), 2)))
            
            # Create investment with random start date (last 30 days)
            days_ago = random.randint(1, 30)
            start_date = timezone.now() - timedelta(days=days_ago)
            
            # Random status (mostly active)
            status_choices = ['active'] * 7 + ['completed'] * 2 + ['pending'] * 1
            status = random.choice(status_choices)
            
            investment = UserInvestment.objects.create(
                user=user,
                investment_plan=plan,
                amount=amount,
                roi_percentage=roi_percentage,
                status=status,
                start_date=start_date
            )
            
            # If completed, set end date in the past
            if status == 'completed':
                investment.end_date = start_date + timedelta(days=plan.duration_days)
                investment.current_value = investment.amount + investment.expected_return
                investment.save()
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created investment {i+1}: {plan.name} - ${amount} ({roi_percentage}% ROI) - {status}'
                )
            )
        
        # Update user portfolio
        portfolio = UserPortfolio.get_or_create_portfolio(user)
        portfolio.update_portfolio_metrics()
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} investments for {username}!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Portfolio Summary:')
        )
        self.stdout.write(f'  Total Invested: ${portfolio.total_invested}')
        self.stdout.write(f'  Current Value: ${portfolio.total_current_value}')
        self.stdout.write(f'  Total Profit: ${portfolio.total_profit}')
        self.stdout.write(f'  ROI: {portfolio.total_roi_percentage}%')
        self.stdout.write(f'  Active Investments: {portfolio.active_investments}')
        self.stdout.write(f'  Completed Investments: {portfolio.completed_investments}')
