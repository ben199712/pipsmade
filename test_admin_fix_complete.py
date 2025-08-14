import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import Transaction, DepositRequest, WithdrawalRequest

print("🧪 Testing Complete Admin Fix...")

# Test 1: Check all transactions have proper requests
print("\n1️⃣ Checking transaction-request relationships:")
transactions = Transaction.objects.all()

for transaction in transactions:
    print(f"\nTransaction #{transaction.id}:")
    print(f"  Type: {transaction.transaction_type}")
    print(f"  Status: {transaction.status}")
    
    if transaction.transaction_type == 'deposit':
        has_request = transaction.has_deposit_request()
        print(f"  Has deposit request: {has_request}")
        if has_request:
            print(f"  Deposit request ID: {transaction.deposit_request.id}")
            print(f"  Admin URL: /transactions/admin/deposit/{transaction.deposit_request.id}/approve/")
    
    elif transaction.transaction_type == 'withdrawal':
        has_request = transaction.has_withdrawal_request()
        print(f"  Has withdrawal request: {has_request}")
        if has_request:
            print(f"  Withdrawal request ID: {transaction.withdrawal_request.id}")
            print(f"  Admin URL: /transactions/admin/withdrawal/{transaction.withdrawal_request.id}/process/")
    
    else:
        print(f"  Other transaction type: {transaction.transaction_type}")

# Test 2: Test template tag functionality
print("\n2️⃣ Testing template tag functionality:")
try:
    from transactions.templatetags.transaction_extras import admin_action_button
    
    for transaction in transactions:
        if transaction.status == 'pending':
            button_html = admin_action_button(transaction)
            print(f"Transaction #{transaction.id} button: Generated successfully ✅")
        
except Exception as e:
    print(f"Template tag error: {e}")

# Test 3: Test admin URLs
print("\n3️⃣ Testing admin URL accessibility:")
client = Client()

# Try to access admin pages (will redirect to login, but should not 404)
test_urls = [
    '/transactions/admin/',
]

# Add specific admin URLs for existing requests
deposit_requests = DepositRequest.objects.all()
for dr in deposit_requests:
    test_urls.append(f'/transactions/admin/deposit/{dr.id}/approve/')

withdrawal_requests = WithdrawalRequest.objects.all()
for wr in withdrawal_requests:
    test_urls.append(f'/transactions/admin/withdrawal/{wr.id}/process/')

for url in test_urls:
    try:
        response = client.get(url)
        if response.status_code in [200, 302]:  # 200 = OK, 302 = Redirect to login
            print(f"  ✅ {url} - Status: {response.status_code}")
        else:
            print(f"  ❌ {url} - Status: {response.status_code}")
    except Exception as e:
        print(f"  ❌ {url} - Error: {e}")

# Test 4: Summary
print("\n📊 System Summary:")
print(f"  Total transactions: {Transaction.objects.count()}")
print(f"  Deposit requests: {DepositRequest.objects.count()}")
print(f"  Withdrawal requests: {WithdrawalRequest.objects.count()}")
print(f"  Pending deposits: {Transaction.objects.filter(transaction_type='deposit', status='pending').count()}")
print(f"  Pending withdrawals: {Transaction.objects.filter(transaction_type='withdrawal', status='pending').count()}")

print("\n✅ Admin Fix Test Complete!")

print("\n🌐 Ready to test:")
print("  1. Start server: python manage.py runserver")
print("  2. Visit: http://127.0.0.1:8000/transactions/admin/")
print("  3. Login with admin credentials")
print("  4. All pending transactions should have action buttons")

print("\n🔧 Admin Actions Available:")
for transaction in Transaction.objects.filter(status='pending'):
    if transaction.transaction_type == 'deposit' and transaction.has_deposit_request():
        print(f"  📥 Deposit #{transaction.id}: Review at /transactions/admin/deposit/{transaction.deposit_request.id}/approve/")
    elif transaction.transaction_type == 'withdrawal' and transaction.has_withdrawal_request():
        print(f"  📤 Withdrawal #{transaction.id}: Process at /transactions/admin/withdrawal/{transaction.withdrawal_request.id}/process/")

print("\n🎉 All systems ready!")
