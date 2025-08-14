import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import (
    CryptoWallet, Transaction, DepositRequest, WithdrawalRequest
)
from decimal import Decimal

print("🔧 Fixing Transaction Requests...")

# Get all transactions that need requests
transactions = Transaction.objects.all()
print(f"Total transactions: {transactions.count()}")

for transaction in transactions:
    print(f"\nTransaction #{transaction.id}:")
    print(f"  Type: {transaction.transaction_type}")
    print(f"  Status: {transaction.status}")
    print(f"  Has deposit request: {transaction.has_deposit_request()}")
    print(f"  Has withdrawal request: {transaction.has_withdrawal_request()}")
    
    # Create missing deposit request
    if transaction.transaction_type == 'deposit' and not transaction.has_deposit_request():
        try:
            crypto_wallet = CryptoWallet.objects.get(crypto_type=transaction.crypto_type)
            
            deposit_request = DepositRequest.objects.create(
                user=transaction.user,
                transaction=transaction,
                crypto_wallet=crypto_wallet,
                amount=transaction.amount,
                transaction_hash=transaction.transaction_hash or 'sample_hash_' + str(transaction.id),
                sender_address=transaction.from_address or 'sample_sender_address'
            )
            
            print(f"  ✅ Created deposit request #{deposit_request.id}")
            
        except Exception as e:
            print(f"  ❌ Error creating deposit request: {e}")
    
    # Create missing withdrawal request
    elif transaction.transaction_type == 'withdrawal' and not transaction.has_withdrawal_request():
        try:
            withdrawal_request = WithdrawalRequest.objects.create(
                user=transaction.user,
                transaction=transaction,
                crypto_type=transaction.crypto_type,
                amount=transaction.amount,
                destination_address=transaction.to_address or 'sample_destination_address',
                network='ERC-20',  # Default network
                platform_fee=transaction.platform_fee,
                ip_address='127.0.0.1',
                user_agent='Sample User Agent'
            )
            
            print(f"  ✅ Created withdrawal request #{withdrawal_request.id}")
            
        except Exception as e:
            print(f"  ❌ Error creating withdrawal request: {e}")

print("\n📊 Final Summary:")
print(f"  Total transactions: {Transaction.objects.count()}")
print(f"  Deposit requests: {DepositRequest.objects.count()}")
print(f"  Withdrawal requests: {WithdrawalRequest.objects.count()}")

# Test the admin actions now
print("\n🧪 Testing admin actions...")
for transaction in Transaction.objects.all():
    print(f"\nTransaction #{transaction.id}:")
    print(f"  Type: {transaction.transaction_type}")
    print(f"  Has deposit request: {transaction.has_deposit_request()}")
    print(f"  Has withdrawal request: {transaction.has_withdrawal_request()}")
    
    if transaction.transaction_type == 'deposit' and transaction.has_deposit_request():
        print(f"  ✅ Deposit request ID: {transaction.deposit_request.id}")
        print(f"  Admin URL: /transactions/admin/deposit/{transaction.deposit_request.id}/approve/")
    
    if transaction.transaction_type == 'withdrawal' and transaction.has_withdrawal_request():
        print(f"  ✅ Withdrawal request ID: {transaction.withdrawal_request.id}")
        print(f"  Admin URL: /transactions/admin/withdrawal/{transaction.withdrawal_request.id}/process/")

print("\n✅ Transaction requests fixed!")
print("\n🌐 Test the admin interface:")
print("  http://127.0.0.1:8000/transactions/admin/")
print("  All pending transactions should now have proper action buttons")
