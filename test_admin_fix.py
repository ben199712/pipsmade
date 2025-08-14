import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from transactions.models import Transaction, DepositRequest, WithdrawalRequest
from django.contrib.auth.models import User

print("🔧 Testing Admin Interface Fix...")

# Test 1: Check existing transactions
print("\n1️⃣ Checking existing transactions:")
transactions = Transaction.objects.all()
print(f"   Total transactions: {transactions.count()}")

for transaction in transactions:
    print(f"   Transaction #{transaction.id}:")
    print(f"     Type: {transaction.transaction_type}")
    print(f"     Status: {transaction.status}")
    print(f"     Has deposit request: {transaction.has_deposit_request()}")
    print(f"     Has withdrawal request: {transaction.has_withdrawal_request()}")
    
    # Test admin actions method
    try:
        from transactions.admin import TransactionAdmin
        admin = TransactionAdmin(Transaction, None)
        actions = admin.admin_actions(transaction)
        print(f"     Admin actions: Works ✅")
    except Exception as e:
        print(f"     Admin actions: Error - {e}")
    print()

# Test 2: Check deposit/withdrawal requests
print("\n2️⃣ Checking deposit/withdrawal requests:")
deposit_requests = DepositRequest.objects.all()
withdrawal_requests = WithdrawalRequest.objects.all()

print(f"   Deposit requests: {deposit_requests.count()}")
print(f"   Withdrawal requests: {withdrawal_requests.count()}")

# Test 3: Create a sample transaction without request (to test the fix)
print("\n3️⃣ Creating test transaction without request:")
try:
    demo_user = User.objects.get(username='demo')
    
    # Create a simple transaction without deposit/withdrawal request
    test_transaction = Transaction.objects.create(
        user=demo_user,
        transaction_type='investment',  # This won't have deposit/withdrawal request
        status='completed',
        amount=100.00,
        crypto_type='USDT',
        user_notes='Test investment transaction'
    )
    
    print(f"   Created test transaction #{test_transaction.id}")
    print(f"   Has deposit request: {test_transaction.has_deposit_request()}")
    print(f"   Has withdrawal request: {test_transaction.has_withdrawal_request()}")
    
    # Test admin actions on this transaction
    try:
        from transactions.admin import TransactionAdmin
        admin = TransactionAdmin(Transaction, None)
        actions = admin.admin_actions(test_transaction)
        print(f"   Admin actions: Works ✅")
    except Exception as e:
        print(f"   Admin actions: Error - {e}")
    
except User.DoesNotExist:
    print("   Demo user not found, skipping test")
except Exception as e:
    print(f"   Error creating test transaction: {e}")

print("\n✅ Admin interface fix test completed!")
print("\n💡 The admin interface should now handle transactions without")
print("   associated deposit/withdrawal requests properly.")

print("\n🌐 Test the admin interface at:")
print("   http://127.0.0.1:8000/admin/transactions/transaction/")
print("   Login with your admin credentials")
