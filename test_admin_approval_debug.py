import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import WithdrawalRequest

print("🔍 Testing Admin Approval with Debug...")

# Create or get admin user
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@pipsmade.com',
        'is_staff': True,
        'is_superuser': True
    }
)

if created or not admin_user.check_password('admin123'):
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✅ Admin user ready: {admin_user.username}")

# Get pending withdrawals
pending_withdrawals = WithdrawalRequest.objects.filter(
    transaction__status='pending'
)

print(f"\n📋 Pending withdrawals: {pending_withdrawals.count()}")

if pending_withdrawals.exists():
    wr = pending_withdrawals.first()
    print(f"   Test withdrawal: #{wr.id} - {wr.amount} {wr.crypto_type}")
    print(f"   Admin URL: http://127.0.0.1:8000/transactions/admin/withdrawal/{wr.id}/process/")
    
    print(f"\n🧪 To test with debug output:")
    print(f"   1. Start server: python manage.py runserver")
    print(f"   2. Login as admin: admin / admin123")
    print(f"   3. Visit: http://127.0.0.1:8000/transactions/admin/withdrawal/{wr.id}/process/")
    print(f"   4. Click 'Approve & Complete Withdrawal'")
    print(f"   5. Check the server console for DEBUG messages")
    
    print(f"\n🔍 Debug messages will show:")
    print(f"   - POST data received")
    print(f"   - Current transaction status")
    print(f"   - User wallet balance")
    print(f"   - Withdrawal amount")
    print(f"   - Balance updates")
    
    print(f"\n📊 Current state:")
    print(f"   Transaction status: {wr.transaction.status}")
    print(f"   User: {wr.user.username}")
    
    # Check user wallet
    from transactions.models import UserWallet
    try:
        wallet = UserWallet.objects.get(user=wr.user, crypto_type=wr.crypto_type)
        print(f"   User wallet balance: {wallet.balance} {wr.crypto_type}")
    except UserWallet.DoesNotExist:
        print(f"   ❌ User wallet not found for {wr.crypto_type}")

else:
    print("   No pending withdrawals found")

print(f"\n🚀 Start the server and test the approval process!")
print(f"   The debug output will help identify where the issue is.")
