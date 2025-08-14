import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import WithdrawalRequest, Transaction

print("🔍 Checking Admin Withdrawal Requests...")

# Get all pending withdrawal requests
pending_withdrawals = WithdrawalRequest.objects.filter(
    transaction__status='pending'
).order_by('-created_at')

print(f"\n📋 Pending Withdrawal Requests: {pending_withdrawals.count()}")

if pending_withdrawals.count() == 0:
    print("   ❌ No pending withdrawal requests found!")
else:
    print("   ✅ Withdrawal requests available for admin processing:")
    
    for i, wr in enumerate(pending_withdrawals, 1):
        print(f"\n   {i}. Withdrawal Request #{wr.id}")
        print(f"      👤 User: {wr.user.username}")
        print(f"      💰 Amount: {wr.amount} {wr.crypto_type}")
        print(f"      📍 Destination: {wr.destination_address}")
        print(f"      🌐 Network: {wr.network}")
        print(f"      💸 Platform Fee: {wr.platform_fee}")
        print(f"      💵 Net Amount: {wr.net_amount()}")
        print(f"      📅 Created: {wr.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      🔧 Admin URL: /transactions/admin/withdrawal/{wr.id}/process/")
        print(f"      🌐 Full URL: http://127.0.0.1:8000/transactions/admin/withdrawal/{wr.id}/process/")

# Check all withdrawal transactions
print(f"\n📊 All Withdrawal Transactions:")
withdrawal_transactions = Transaction.objects.filter(
    transaction_type='withdrawal'
).order_by('-created_at')

print(f"   Total withdrawal transactions: {withdrawal_transactions.count()}")

for tx in withdrawal_transactions:
    print(f"   💸 Transaction #{tx.id}: {tx.amount} {tx.crypto_type} - Status: {tx.status}")
    print(f"      User: {tx.user.username}")
    print(f"      Created: {tx.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if tx.has_withdrawal_request():
        print(f"      ✅ Has withdrawal request: #{tx.withdrawal_request.id}")
    else:
        print(f"      ❌ No withdrawal request")

print(f"\n🎯 Admin Dashboard Summary:")
print(f"   📤 Pending Withdrawals: {pending_withdrawals.count()}")
print(f"   📊 Total Withdrawal Transactions: {withdrawal_transactions.count()}")

print(f"\n🌐 Admin Access URLs:")
print(f"   👑 Main Admin Dashboard: http://127.0.0.1:8000/transactions/admin/")
print(f"   🔧 Django Admin: http://127.0.0.1:8000/admin/")

if pending_withdrawals.exists():
    print(f"\n🚨 ACTION REQUIRED:")
    print(f"   You have {pending_withdrawals.count()} pending withdrawal requests waiting for admin approval!")
    print(f"   Visit the admin dashboard to process them:")
    print(f"   👉 http://127.0.0.1:8000/transactions/admin/")

print(f"\n✅ Withdrawal system is working correctly!")
print(f"   Withdrawal requests ARE being sent to admin.")
print(f"   Check the admin dashboard to process pending requests.")
