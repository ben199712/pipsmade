import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import (
    CryptoWallet, UserWallet, Transaction, 
    DepositRequest, WithdrawalRequest
)
from decimal import Decimal

print("🔧 Creating Sample Deposit and Withdrawal Requests...")

try:
    demo_user = User.objects.get(username='demo')
    print(f"✅ Found demo user: {demo_user.username}")
    
    # Get crypto wallets
    btc_wallet = CryptoWallet.objects.get(crypto_type='BTC')
    eth_wallet = CryptoWallet.objects.get(crypto_type='ETH')
    
    # 1. Create a sample deposit request
    print("\n💰 Creating sample deposit request...")
    
    # Create transaction for deposit
    deposit_transaction = Transaction.objects.create(
        user=demo_user,
        transaction_type='deposit',
        status='pending',
        amount=Decimal('0.01000000'),
        crypto_type='BTC',
        transaction_hash='1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890',
        to_address=btc_wallet.wallet_address,
        from_address='1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
        user_notes='Sample deposit request'
    )
    
    # Create deposit request
    deposit_request = DepositRequest.objects.create(
        user=demo_user,
        transaction=deposit_transaction,
        crypto_wallet=btc_wallet,
        amount=Decimal('0.01000000'),
        transaction_hash='1a2b3c4d5e6f7890abcdef1234567890abcdef1234567890abcdef1234567890',
        sender_address='1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'
    )
    
    print(f"✅ Created deposit request #{deposit_request.id}")
    print(f"   Transaction: #{deposit_transaction.id}")
    print(f"   Amount: {deposit_request.amount} BTC")
    
    # 2. Create a sample withdrawal request
    print("\n💸 Creating sample withdrawal request...")
    
    # Create transaction for withdrawal
    withdrawal_transaction = Transaction.objects.create(
        user=demo_user,
        transaction_type='withdrawal',
        status='pending',
        amount=Decimal('0.50000000'),
        crypto_type='ETH',
        to_address='0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
        platform_fee=Decimal('0.01000000'),
        user_notes='Sample withdrawal request'
    )
    
    # Create withdrawal request
    withdrawal_request = WithdrawalRequest.objects.create(
        user=demo_user,
        transaction=withdrawal_transaction,
        crypto_type='ETH',
        amount=Decimal('0.50000000'),
        destination_address='0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
        network='ERC-20',
        platform_fee=Decimal('0.01000000'),
        ip_address='127.0.0.1',
        user_agent='Test User Agent'
    )
    
    print(f"✅ Created withdrawal request #{withdrawal_request.id}")
    print(f"   Transaction: #{withdrawal_transaction.id}")
    print(f"   Amount: {withdrawal_request.amount} ETH")
    
    print("\n📊 Summary:")
    print(f"   Total transactions: {Transaction.objects.count()}")
    print(f"   Deposit requests: {DepositRequest.objects.count()}")
    print(f"   Withdrawal requests: {WithdrawalRequest.objects.count()}")
    
    print("\n🌐 Test the admin interface:")
    print("   http://127.0.0.1:8000/admin/transactions/transaction/")
    print("   http://127.0.0.1:8000/admin/transactions/depositrequest/")
    print("   http://127.0.0.1:8000/admin/transactions/withdrawalrequest/")
    
    print("\n✅ Sample requests created successfully!")
    
except User.DoesNotExist:
    print("❌ Demo user not found. Run create_demo_user.py first.")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
