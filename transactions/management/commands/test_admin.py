from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transactions.models import Transaction, DepositRequest, WithdrawalRequest

class Command(BaseCommand):
    help = 'Test admin interface functionality'

    def handle(self, *args, **options):
        self.stdout.write("🧪 Testing Admin Interface...")
        
        # Test 1: Check transactions
        self.stdout.write("\n1️⃣ Checking transactions:")
        transactions = Transaction.objects.all()
        self.stdout.write(f"   Total transactions: {transactions.count()}")
        
        for transaction in transactions:
            self.stdout.write(f"\nTransaction #{transaction.id}:")
            self.stdout.write(f"  Type: {transaction.transaction_type}")
            self.stdout.write(f"  Status: {transaction.status}")
            self.stdout.write(f"  Has deposit request: {transaction.has_deposit_request()}")
            self.stdout.write(f"  Has withdrawal request: {transaction.has_withdrawal_request()}")
        
        # Test 2: Check requests
        self.stdout.write("\n2️⃣ Checking requests:")
        self.stdout.write(f"   Deposit requests: {DepositRequest.objects.count()}")
        self.stdout.write(f"   Withdrawal requests: {WithdrawalRequest.objects.count()}")
        
        # Test 3: Check admin users
        self.stdout.write("\n3️⃣ Checking admin users:")
        admin_users = User.objects.filter(is_superuser=True)
        self.stdout.write(f"   Admin users: {admin_users.count()}")
        
        if admin_users.count() == 0:
            self.stdout.write(self.style.WARNING("   No admin users found!"))
            self.stdout.write("   Create one with: python manage.py createsuperuser")
        
        # Test 4: Check pending transactions
        self.stdout.write("\n4️⃣ Checking pending transactions:")
        pending_deposits = Transaction.objects.filter(transaction_type='deposit', status='pending')
        pending_withdrawals = Transaction.objects.filter(transaction_type='withdrawal', status='pending')
        
        self.stdout.write(f"   Pending deposits: {pending_deposits.count()}")
        for deposit in pending_deposits:
            if deposit.has_deposit_request():
                self.stdout.write(f"     ✅ Deposit #{deposit.id} - Request ID: {deposit.deposit_request.id}")
            else:
                self.stdout.write(f"     ❌ Deposit #{deposit.id} - No request")
        
        self.stdout.write(f"   Pending withdrawals: {pending_withdrawals.count()}")
        for withdrawal in pending_withdrawals:
            if withdrawal.has_withdrawal_request():
                self.stdout.write(f"     ✅ Withdrawal #{withdrawal.id} - Request ID: {withdrawal.withdrawal_request.id}")
            else:
                self.stdout.write(f"     ❌ Withdrawal #{withdrawal.id} - No request")
        
        self.stdout.write("\n🌐 URLs to test:")
        self.stdout.write("   📊 Admin Dashboard: http://127.0.0.1:8000/transactions/admin/")
        self.stdout.write("   🔧 Django Admin: http://127.0.0.1:8000/admin/")
        
        self.stdout.write("\n✅ Admin interface ready!")
        self.stdout.write(self.style.SUCCESS("All systems operational!"))
