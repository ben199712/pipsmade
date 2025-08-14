import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import Transaction, WithdrawalRequest, DepositRequest

print("🧪 Testing Transaction Templates...")

# Create test client
client = Client()

# Test 1: Login as demo user
print("\n1️⃣ Testing user authentication...")
try:
    demo_user = User.objects.get(username='demo')
    login_success = client.login(username='demo', password='demo123')
    print(f"   Login successful: {login_success}")
    
    if login_success:
        # Test transactions page
        response = client.get('/transactions/')
        print(f"   Transactions page: {response.status_code}")
        
        # Test deposit page
        response = client.get('/transactions/deposit/')
        print(f"   Deposit page: {response.status_code}")
        
        # Test withdrawal page
        response = client.get('/transactions/withdrawal/')
        print(f"   Withdrawal page: {response.status_code}")
        
        # Test transaction detail
        transactions = Transaction.objects.filter(user=demo_user)
        if transactions.exists():
            transaction = transactions.first()
            response = client.get(f'/transactions/{transaction.id}/')
            print(f"   Transaction detail page: {response.status_code}")
        
except User.DoesNotExist:
    print("   Demo user not found")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Check if admin templates exist
print("\n2️⃣ Checking template files...")
template_files = [
    'templates/transactions/transactions.html',
    'templates/transactions/deposit.html', 
    'templates/transactions/withdrawal.html',
    'templates/transactions/transaction_detail.html',
    'templates/transactions/admin_transactions.html',
    'templates/transactions/admin_approve_deposit.html',
    'templates/transactions/admin_process_withdrawal.html'
]

for template_file in template_files:
    if os.path.exists(template_file):
        print(f"   ✅ {template_file}")
    else:
        print(f"   ❌ {template_file}")

# Test 3: Check withdrawal requests for admin processing
print("\n3️⃣ Checking withdrawal requests...")
withdrawal_requests = WithdrawalRequest.objects.all()
print(f"   Total withdrawal requests: {withdrawal_requests.count()}")

for wr in withdrawal_requests:
    print(f"   Withdrawal #{wr.id}: {wr.crypto_type} - {wr.transaction.status}")
    admin_url = f"/transactions/admin/withdrawal/{wr.id}/process/"
    print(f"   Admin URL: {admin_url}")

# Test 4: Check deposit requests
print("\n4️⃣ Checking deposit requests...")
deposit_requests = DepositRequest.objects.all()
print(f"   Total deposit requests: {deposit_requests.count()}")

for dr in deposit_requests:
    print(f"   Deposit #{dr.id}: {dr.crypto_wallet.crypto_type} - {dr.transaction.status}")
    admin_url = f"/transactions/admin/deposit/{dr.id}/approve/"
    print(f"   Admin URL: {admin_url}")

print("\n✅ Template testing completed!")
print("\n🌐 Available URLs:")
print("   📊 User Transactions: http://127.0.0.1:8000/transactions/")
print("   💰 Deposit: http://127.0.0.1:8000/transactions/deposit/")
print("   💸 Withdrawal: http://127.0.0.1:8000/transactions/withdrawal/")
print("   👑 Admin Transactions: http://127.0.0.1:8000/transactions/admin/")
print("   🔧 Django Admin: http://127.0.0.1:8000/admin/")

print("\n🚀 Start server: python manage.py runserver")
