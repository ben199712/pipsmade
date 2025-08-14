import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import UserWallet, Transaction, WithdrawalRequest
from decimal import Decimal

print("🔍 Debugging Withdrawal Approval Process...")

try:
    # Get demo user and admin user
    demo_user = User.objects.get(username='demo')
    
    # Try to get or create an admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pipsmade.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"✅ Found admin user: {admin_user.username}")
    
    # Check current state
    print(f"\n📊 Current State:")
    
    # User wallet balances
    user_wallets = UserWallet.objects.filter(user=demo_user)
    print(f"   User Wallet Balances:")
    for wallet in user_wallets:
        print(f"     {wallet.crypto_type}: {wallet.balance}")
    
    # Pending withdrawals
    pending_withdrawals = WithdrawalRequest.objects.filter(
        user=demo_user,
        transaction__status='pending'
    )
    print(f"\n   Pending Withdrawals: {pending_withdrawals.count()}")
    
    if pending_withdrawals.count() == 0:
        print("   No pending withdrawals found. Creating one for testing...")
        
        # Ensure user has BTC balance
        btc_wallet, created = UserWallet.objects.get_or_create(
            user=demo_user,
            crypto_type='BTC',
            defaults={'balance': Decimal('1.0')}
        )
        if btc_wallet.balance < Decimal('0.1'):
            btc_wallet.balance = Decimal('1.0')
            btc_wallet.save()
        
        # Create test withdrawal
        from transactions.models import CryptoWallet
        crypto_wallet = CryptoWallet.objects.get(crypto_type='BTC')
        amount = Decimal('0.05')
        platform_fee = amount * (crypto_wallet.withdrawal_fee_percentage / 100)
        
        transaction = Transaction.objects.create(
            user=demo_user,
            transaction_type='withdrawal',
            status='pending',
            amount=amount,
            crypto_type='BTC',
            to_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            platform_fee=platform_fee,
            user_notes='Debug test withdrawal'
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
            user_agent='Debug Test'
        )
        
        print(f"   ✅ Created test withdrawal request #{withdrawal_request.id}")
        pending_withdrawals = [withdrawal_request]
    
    # Test the approval process programmatically
    print(f"\n🧪 Testing Approval Process:")
    
    test_withdrawal = pending_withdrawals[0]
    print(f"   Testing withdrawal #{test_withdrawal.id}")
    print(f"   Amount: {test_withdrawal.amount} {test_withdrawal.crypto_type}")
    print(f"   Current transaction status: {test_withdrawal.transaction.status}")
    
    # Get current balance before approval
    user_wallet = UserWallet.objects.get(
        user=demo_user,
        crypto_type=test_withdrawal.crypto_type
    )
    balance_before = user_wallet.balance
    print(f"   User balance before: {balance_before}")
    
    # Simulate admin approval using the client
    client = Client()
    
    # Login as admin
    admin_login = client.login(username='admin', password='admin123')
    print(f"   Admin login successful: {admin_login}")
    
    if admin_login:
        # Test GET request to admin page
        admin_url = f'/transactions/admin/withdrawal/{test_withdrawal.id}/process/'
        response = client.get(admin_url)
        print(f"   Admin page status: {response.status_code}")
        
        if response.status_code == 200:
            # Test POST request to approve withdrawal
            approval_data = {
                'action': 'approve',
                'admin_notes': 'Debug test approval'
            }
            
            print(f"   Submitting approval...")
            response = client.post(admin_url, approval_data)
            print(f"   Approval response status: {response.status_code}")
            
            # Check if it redirected (success)
            if response.status_code == 302:
                print(f"   ✅ Approval submitted successfully (redirected)")
                
                # Refresh objects from database
                test_withdrawal.refresh_from_db()
                test_withdrawal.transaction.refresh_from_db()
                user_wallet.refresh_from_db()
                
                print(f"\n📊 After Approval:")
                print(f"   Transaction status: {test_withdrawal.transaction.status}")
                print(f"   User balance after: {user_wallet.balance}")
                print(f"   Balance change: {balance_before - user_wallet.balance}")
                
                if test_withdrawal.transaction.status == 'completed':
                    print(f"   ✅ SUCCESS: Transaction marked as completed!")
                else:
                    print(f"   ❌ ISSUE: Transaction still shows as {test_withdrawal.transaction.status}")
                
                if user_wallet.balance < balance_before:
                    print(f"   ✅ SUCCESS: User balance was deducted!")
                else:
                    print(f"   ❌ ISSUE: User balance was not deducted!")
                    
            else:
                print(f"   ❌ Approval failed with status: {response.status_code}")
                if hasattr(response, 'content'):
                    print(f"   Response content: {response.content[:500]}")
        else:
            print(f"   ❌ Could not access admin page: {response.status_code}")
    else:
        print(f"   ❌ Admin login failed")
    
    print(f"\n🌐 Manual Testing URLs:")
    print(f"   Admin Dashboard: http://127.0.0.1:8000/transactions/admin/")
    print(f"   Process Withdrawal: http://127.0.0.1:8000{admin_url}")
    print(f"   User Dashboard: http://127.0.0.1:8000/dashboard/")
    print(f"   User Transactions: http://127.0.0.1:8000/transactions/")
    
    print(f"\n🔑 Login Credentials:")
    print(f"   Admin: admin / admin123")
    print(f"   User: demo / demo123")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
