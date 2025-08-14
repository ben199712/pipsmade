import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import (
    CryptoWallet, UserWallet, Transaction, WithdrawalRequest
)
from decimal import Decimal

print("🧪 Creating Test Withdrawal Request...")

try:
    # Get demo user
    demo_user = User.objects.get(username='demo')
    print(f"✅ Found demo user: {demo_user.username}")
    
    # Check/create user wallet with balance
    btc_wallet, created = UserWallet.objects.get_or_create(
        user=demo_user,
        crypto_type='BTC',
        defaults={'balance': Decimal('0.5')}
    )
    
    if created:
        print(f"✅ Created BTC wallet with balance: {btc_wallet.balance}")
    else:
        if btc_wallet.balance < Decimal('0.1'):
            btc_wallet.balance = Decimal('0.5')
            btc_wallet.save()
            print(f"✅ Updated BTC wallet balance: {btc_wallet.balance}")
        else:
            print(f"✅ BTC wallet exists with balance: {btc_wallet.balance}")
    
    # Get crypto wallet for fees
    crypto_wallet = CryptoWallet.objects.get(crypto_type='BTC')
    print(f"✅ Found crypto wallet: {crypto_wallet.crypto_type} (Fee: {crypto_wallet.withdrawal_fee_percentage}%)")
    
    # Create withdrawal transaction
    amount = Decimal('0.05')
    platform_fee = amount * (crypto_wallet.withdrawal_fee_percentage / 100)
    destination_address = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
    
    transaction = Transaction.objects.create(
        user=demo_user,
        transaction_type='withdrawal',
        status='pending',
        amount=amount,
        crypto_type='BTC',
        to_address=destination_address,
        platform_fee=platform_fee,
        user_notes=f"Test withdrawal to {destination_address[:20]}..."
    )
    
    print(f"✅ Created transaction #{transaction.id}")
    
    # Create withdrawal request
    withdrawal_request = WithdrawalRequest.objects.create(
        user=demo_user,
        transaction=transaction,
        crypto_type='BTC',
        amount=amount,
        destination_address=destination_address,
        network='BTC',
        platform_fee=platform_fee,
        ip_address='127.0.0.1',
        user_agent='Test User Agent'
    )
    
    print(f"✅ Created withdrawal request #{withdrawal_request.id}")
    
    # Verify the request was created
    print("\n📊 Verification:")
    print(f"   Transaction ID: {transaction.id}")
    print(f"   Transaction Status: {transaction.status}")
    print(f"   Withdrawal Request ID: {withdrawal_request.id}")
    print(f"   Amount: {withdrawal_request.amount} {withdrawal_request.crypto_type}")
    print(f"   Destination: {withdrawal_request.destination_address}")
    print(f"   Platform Fee: {withdrawal_request.platform_fee}")
    print(f"   Net Amount: {withdrawal_request.net_amount()}")
    
    # Check admin URL
    admin_url = f"/transactions/admin/withdrawal/{withdrawal_request.id}/process/"
    print(f"\n🔧 Admin URL: {admin_url}")
    
    # Check all withdrawal requests
    all_withdrawals = WithdrawalRequest.objects.filter(user=demo_user)
    print(f"\n📋 Total withdrawal requests for {demo_user.username}: {all_withdrawals.count()}")
    
    for wr in all_withdrawals:
        print(f"   📤 Request #{wr.id}: {wr.amount} {wr.crypto_type} - Status: {wr.transaction.status}")
        print(f"      Created: {wr.created_at}")
        print(f"      Admin URL: /transactions/admin/withdrawal/{wr.id}/process/")
    
    print("\n✅ Test withdrawal request created successfully!")
    print("\n🌐 Test URLs:")
    print("   📊 Transactions: http://127.0.0.1:8000/transactions/")
    print("   📤 Withdrawal: http://127.0.0.1:8000/transactions/withdrawal/")
    print("   👑 Admin: http://127.0.0.1:8000/transactions/admin/")
    print(f"   🔧 Process: http://127.0.0.1:8000{admin_url}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
