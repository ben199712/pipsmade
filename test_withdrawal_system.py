import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import (
    CryptoWallet, UserWallet, Transaction, WithdrawalRequest
)
from decimal import Decimal

print("🧪 Testing Withdrawal System...")

# Test 1: Check if demo user has wallet balances
print("\n1️⃣ Checking user wallet balances:")
try:
    demo_user = User.objects.get(username='demo')
    user_wallets = UserWallet.objects.filter(user=demo_user, balance__gt=0)
    
    print(f"   Demo user found: {demo_user.username}")
    print(f"   Wallets with balance: {user_wallets.count()}")
    
    for wallet in user_wallets:
        print(f"   💰 {wallet.crypto_type}: {wallet.balance}")
    
    if user_wallets.count() == 0:
        print("   ⚠️  No wallets with balance found!")
        print("   Creating sample balance for testing...")
        
        # Create a sample balance
        btc_wallet, created = UserWallet.objects.get_or_create(
            user=demo_user,
            crypto_type='BTC',
            defaults={'balance': Decimal('0.1')}
        )
        if created:
            print(f"   ✅ Created BTC wallet with balance: {btc_wallet.balance}")
        else:
            btc_wallet.balance = Decimal('0.1')
            btc_wallet.save()
            print(f"   ✅ Updated BTC wallet balance: {btc_wallet.balance}")

except User.DoesNotExist:
    print("   ❌ Demo user not found!")
    return

# Test 2: Check crypto wallets for withdrawal fees
print("\n2️⃣ Checking crypto wallets:")
crypto_wallets = CryptoWallet.objects.all()
print(f"   Available crypto wallets: {crypto_wallets.count()}")

for wallet in crypto_wallets:
    print(f"   🏦 {wallet.crypto_type}: Fee {wallet.withdrawal_fee_percentage}%")

# Test 3: Test withdrawal form submission
print("\n3️⃣ Testing withdrawal form submission:")
client = Client()

# Login as demo user
login_success = client.login(username='demo', password='demo123')
print(f"   Login successful: {login_success}")

if login_success:
    # Test GET request to withdrawal page
    response = client.get('/transactions/withdrawal/')
    print(f"   Withdrawal page status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Withdrawal page loads successfully")
        
        # Test POST request with withdrawal data
        withdrawal_data = {
            'crypto_type': 'BTC',
            'amount': '0.01',
            'destination_address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'network': 'BTC',
            'confirm_address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        }
        
        print("   Submitting withdrawal request...")
        response = client.post('/transactions/withdrawal/', withdrawal_data)
        print(f"   POST response status: {response.status_code}")
        
        if response.status_code == 302:  # Redirect after successful submission
            print("   ✅ Withdrawal form submitted successfully (redirected)")
        else:
            print(f"   ⚠️  Unexpected response: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"   Response content preview: {response.content[:200]}")
    else:
        print(f"   ❌ Withdrawal page failed to load: {response.status_code}")

# Test 4: Check if withdrawal requests were created
print("\n4️⃣ Checking withdrawal requests:")
withdrawal_requests = WithdrawalRequest.objects.filter(user=demo_user)
print(f"   Total withdrawal requests: {withdrawal_requests.count()}")

for wr in withdrawal_requests:
    print(f"   📤 Request #{wr.id}: {wr.amount} {wr.crypto_type} - Status: {wr.transaction.status}")
    print(f"      Created: {wr.created_at}")
    print(f"      Destination: {wr.destination_address}")

# Test 5: Check transactions
print("\n5️⃣ Checking withdrawal transactions:")
withdrawal_transactions = Transaction.objects.filter(
    user=demo_user, 
    transaction_type='withdrawal'
)
print(f"   Total withdrawal transactions: {withdrawal_transactions.count()}")

for tx in withdrawal_transactions:
    print(f"   💸 Transaction #{tx.id}: {tx.amount} {tx.crypto_type} - Status: {tx.status}")
    print(f"      Created: {tx.created_at}")
    print(f"      Has withdrawal request: {tx.has_withdrawal_request()}")

# Test 6: Check admin URLs
print("\n6️⃣ Testing admin URLs:")
if withdrawal_requests.exists():
    for wr in withdrawal_requests:
        admin_url = f"/transactions/admin/withdrawal/{wr.id}/process/"
        print(f"   🔧 Admin URL: {admin_url}")
        
        # Test admin URL accessibility
        response = client.get(admin_url)
        print(f"   Admin page status: {response.status_code}")

print("\n📊 Summary:")
print(f"   User wallets: {UserWallet.objects.filter(user=demo_user).count()}")
print(f"   Withdrawal requests: {WithdrawalRequest.objects.filter(user=demo_user).count()}")
print(f"   Withdrawal transactions: {Transaction.objects.filter(user=demo_user, transaction_type='withdrawal').count()}")

print("\n🌐 URLs to test manually:")
print("   📤 Withdrawal page: http://127.0.0.1:8000/transactions/withdrawal/")
print("   📊 Transactions: http://127.0.0.1:8000/transactions/")
print("   👑 Admin: http://127.0.0.1:8000/transactions/admin/")

print("\n✅ Withdrawal system test completed!")
