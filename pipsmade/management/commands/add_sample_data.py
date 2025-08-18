from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from investments.models import UserPortfolio, UserInvestment, InvestmentReturn
from transactions.models import Transaction, UserWallet
import random

class Command(BaseCommand):
    help = 'Add sample data for testing portfolio charts'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to add sample data for')
        parser.add_argument('--amount', type=float, default=1000.0, help='Base amount for sample data')

    def handle(self, *args, **options):
        username = options['username']
        base_amount = Decimal(str(options['amount']))
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))
            return
        
        self.stdout.write(f'Adding sample data for user: {username}')
        
        # Get or create portfolio
        portfolio, created = UserPortfolio.objects.get_or_create(
            user=user,
            defaults={
                'total_invested': base_amount,
                'total_current_value': base_amount,
                'total_profit': 0,
                'total_roi_percentage': 0,
                'total_withdrawable': base_amount,
                'active_investments': 1,
                'manual_profit_total': 0
            }
        )
        
        if created:
            self.stdout.write(f'Created new portfolio for {username}')
        else:
            self.stdout.write(f'Using existing portfolio for {username}')
        
        # Add sample investment returns over the last 30 days
        for i in range(30):
            date = timezone.now().date() - timedelta(days=29-i)
            
            # Generate some random daily returns
            daily_return = Decimal(str(random.uniform(-50, 100)))
            
            # Create investment return record
            InvestmentReturn.objects.get_or_create(
                investment__user=user,
                date=date,
                defaults={
                    'daily_return': daily_return,
                    'notes': f'Sample daily return for {date}'
                }
            )
        
        # Add some manual profits
        manual_profits = [250, 180, 320, 150, 400, 280, 350, 200, 300, 220]
        for i, profit in enumerate(manual_profits):
            date = timezone.now().date() - timedelta(days=29-i*3)  # Spread out over time
            
            # Update portfolio with manual profit
            portfolio.manual_profit_total += Decimal(str(profit))
            portfolio.total_profit += Decimal(str(profit))
            portfolio.total_current_value += Decimal(str(profit))
            portfolio.total_withdrawable += Decimal(str(profit))
            portfolio.save()
            
            self.stdout.write(f'Added manual profit ${profit} for {date}')
        
        # Add some sample transactions
        transaction_types = ['deposit', 'withdrawal']
        for i in range(10):
            trans_type = random.choice(transaction_types)
            amount = Decimal(str(random.uniform(100, 500)))
            date = timezone.now() - timedelta(days=random.randint(1, 28))
            
            Transaction.objects.get_or_create(
                user=user,
                transaction_type=trans_type,
                amount=amount,
                usd_equivalent=amount,
                status='completed',
                created_at=timezone.now().replace(date=date),
                defaults={
                    'crypto_type': 'USD',
                    'to_address': 'sample_address',
                    'from_address': 'sample_address'
                }
            )
            
            self.stdout.write(f'Added {trans_type} transaction: ${amount} for {date}')
        
        # Update portfolio metrics
        portfolio.total_roi_percentage = (portfolio.total_profit / portfolio.total_invested * 100) if portfolio.total_invested > 0 else 0
        portfolio.save()
        
        self.stdout.write(self.style.SUCCESS(f'Sample data added successfully for {username}'))
        self.stdout.write(f'Portfolio summary:')
        self.stdout.write(f'  Total Invested: ${portfolio.total_invested}')
        self.stdout.write(f'  Total Current Value: ${portfolio.total_current_value}')
        self.stdout.write(f'  Total Profit: ${portfolio.total_profit}')
        self.stdout.write(f'  ROI: {portfolio.total_roi_percentage:.2f}%')
        self.stdout.write(f'  Manual Profit Total: ${portfolio.manual_profit_total}')
        self.stdout.write(f'  Total Withdrawable: ${portfolio.total_withdrawable}') 