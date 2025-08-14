import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import (
    UserWallet, Transaction, WithdrawalRequest
)
from decimal import Decimal

print("🧪 Testing Withdrawal Approval Fix...")

try:
    # Get demo user
    demo_user = User.objects.get(username='demo')
    print(f"✅ Found demo user: {demo_user.username}")
    
    # Check current wallet balance
    try:
        btc_wallet = UserWallet.objects.get(user=demo_user, crypto_type='BTC')
        print(f"💰 Current BTC balance: {btc_wallet.balance}")
    except UserWallet.DoesNotExist:
        # Create wallet with balance for testing
        btc_wallet = UserWallet.objects.create(
            user=demo_user,
            crypto_type='BTC',
            balance=Decimal('1.0')
        )
        print(f"💰 Created BTC wallet with balance: {btc_wallet.balance}")
    
    # Check pending withdrawal requests
    pending_withdrawals = WithdrawalRequest.objects.filter(
        user=demo_user,
        transaction__status='pending'
    )
    
    print(f"\n📋 Pending withdrawal requests: {pending_withdrawals.count()}")
    
    if pending_withdrawals.count() == 0:
        print("   Creating a test withdrawal request...")
        
        # Create a test withdrawal
        from transactions.models import CryptoWallet
        crypto_wallet = CryptoWallet.objects.get(crypto_type='BTC')
        amount = Decimal('0.1')
        platform_fee = amount * (crypto_wallet.withdrawal_fee_percentage / 100)
        
        transaction = Transaction.objects.create(
            user=demo_user,
            transaction_type='withdrawal',
            status='pending',
            amount=amount,
            crypto_type='BTC',
            to_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            platform_fee=platform_fee,
            user_notes='Test withdrawal for approval'
        )
        
        withdrawal_request = WithdrawalRequest.objects.create(
            user=demo_user,
            transaction=transaction,
            crypto_type='BTC',
            amount=amount,
            destination_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            network='BTC',
            platform_fee=platform_fee,
            ip_address='127.0.0.1',
            user_agent='Test User Agent'
        )
        
        print(f"   ✅ Created test withdrawal request #{withdrawal_request.id}")
        pending_withdrawals = [withdrawal_request]
    
    # Show what admin will see
    print(f"\n🔧 Admin Dashboard Preview:")
    for wr in pending_withdrawals:
        print(f"   📤 Withdrawal Request #{wr.id}")
        print(f"      User: {wr.user.username}")
        print(f"      Amount: {wr.amount} {wr.crypto_type}")
        print(f"      Current Status: {wr.transaction.status}")
        print(f"      Admin URL: http://127.0.0.1:8000/transactions/admin/withdrawal/{wr.id}/process/")
    
    # Show current state
    print(f"\n📊 Current State:")
    print(f"   User BTC Balance: {btc_wallet.balance}")
    print(f"   Pending Withdrawals: {pending_withdrawals.count()}")
    
    # Show what will happen after approval
    if pending_withdrawals:
        wr = pending_withdrawals[0]
        new_balance = btc_wallet.balance - wr.amount
        print(f"\n🎯 After Approval:")
        print(f"   Withdrawal Amount: {wr.amount} BTC")
        print(f"   New User Balance: {new_balance} BTC")
        print(f"   Transaction Status: completed")
        print(f"   User Dashboard: Will show updated balance and completed transaction")
    
    print(f"\n🚀 Test the Fix:")
    print(f"   1. Start server: python manage.py runserver")
    print(f"   2. Visit admin: http://127.0.0.1:8000/transactions/admin/")
    print(f"   3. Click 'Process' on pending withdrawal")
    print(f"   4. Click 'Approve & Complete Withdrawal'")
    print(f"   5. Confirm in modal")
    print(f"   6. Check user dashboard: http://127.0.0.1:8000/dashboard/")
    print(f"   7. Check transactions: http://127.0.0.1:8000/transactions/")
    
    print(f"\n✅ The fix should now:")
    print(f"   ✅ Deduct amount from user wallet immediately")
    print(f"   ✅ Mark transaction as 'completed'")
    print(f"   ✅ Update user dashboard balance")
    print(f"   ✅ Show completed transaction in history")
    print(f"   ✅ Send notification to user")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
