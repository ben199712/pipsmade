import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import UserWallet, Transaction

print("📊 User Dashboard State Check...")

try:
    demo_user = User.objects.get(username='demo')
    
    print(f"\n👤 User: {demo_user.username}")
    
    # Show current wallet balances
    print(f"\n💰 Current Wallet Balances:")
    user_wallets = UserWallet.objects.filter(user=demo_user)
    
    if user_wallets.exists():
        for wallet in user_wallets:
            print(f"   {wallet.crypto_type}: {wallet.balance}")
    else:
        print("   No wallet balances found")
    
    # Show transaction history
    print(f"\n📋 Transaction History:")
    transactions = Transaction.objects.filter(user=demo_user).order_by('-created_at')
    
    if transactions.exists():
        for tx in transactions:
            print(f"   #{tx.id}: {tx.get_transaction_type_display()} - {tx.amount} {tx.crypto_type} - {tx.get_status_display()}")
            print(f"        Created: {tx.created_at.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("   No transactions found")
    
    # Show pending transactions specifically
    pending_transactions = transactions.filter(status='pending')
    print(f"\n⏳ Pending Transactions: {pending_transactions.count()}")
    for tx in pending_transactions:
        print(f"   #{tx.id}: {tx.get_transaction_type_display()} - {tx.amount} {tx.crypto_type}")
    
    # Show completed transactions
    completed_transactions = transactions.filter(status='completed')
    print(f"\n✅ Completed Transactions: {completed_transactions.count()}")
    for tx in completed_transactions:
        print(f"   #{tx.id}: {tx.get_transaction_type_display()} - {tx.amount} {tx.crypto_type}")
    
    print(f"\n🎯 What User Should See After Withdrawal Approval:")
    print(f"   1. Wallet Balance: Will decrease by withdrawal amount")
    print(f"   2. Transaction Status: Will change from 'Pending' to 'Completed'")
    print(f"   3. Transaction History: Will show the completed withdrawal")
    print(f"   4. Dashboard: Will reflect new balance immediately")
    
    print(f"\n🔍 To verify the fix works:")
    print(f"   1. Note current balances above")
    print(f"   2. Approve a withdrawal in admin")
    print(f"   3. Refresh user dashboard")
    print(f"   4. Check that balance decreased")
    print(f"   5. Check that transaction shows as 'Completed'")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
