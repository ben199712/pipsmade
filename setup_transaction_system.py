#!/usr/bin/env python
"""
Script to set up the complete transaction system for pipsmade
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from transactions.models import CryptoWallet, UserWallet, Transaction
from decimal import Decimal

def main():
    print("🚀 Setting up Transaction System for pipsmade...")
    
    # 1. Run migrations
    print("\n📊 Running database migrations...")
    try:
        call_command('makemigrations', 'transactions')
        call_command('migrate')
        print("✅ Database migrations completed")
    except Exception as e:
        print(f"⚠️  Migration warning: {e}")
    
    # 2. Set up crypto wallets
    print("\n💰 Setting up crypto wallets...")
    call_command('setup_crypto_wallets')
    
    # 3. Create sample user wallets for demo user
    print("\n👤 Setting up demo user wallets...")
    try:
        demo_user = User.objects.get(username='demo')
        
        # Create sample balances for demo user
        sample_balances = [
            {'crypto_type': 'BTC', 'balance': Decimal('0.15000000')},
            {'crypto_type': 'ETH', 'balance': Decimal('2.50000000')},
            {'crypto_type': 'USDT', 'balance': Decimal('1500.00000000')},
            {'crypto_type': 'BNB', 'balance': Decimal('10.00000000')},
        ]
        
        for balance_data in sample_balances:
            wallet, created = UserWallet.objects.get_or_create(
                user=demo_user,
                crypto_type=balance_data['crypto_type'],
                defaults={'balance': balance_data['balance']}
            )
            if created:
                print(f"✅ Created {balance_data['crypto_type']} wallet: {balance_data['balance']}")
            else:
                print(f"⚠️  {balance_data['crypto_type']} wallet already exists")
        
        print(f"✅ Demo user wallets set up successfully!")
        
    except User.DoesNotExist:
        print("⚠️  Demo user not found. Run create_demo_user.py first.")
    
    # 4. Create sample transactions
    print("\n📝 Creating sample transactions...")
    try:
        demo_user = User.objects.get(username='demo')
        
        # Sample completed deposit
        if not Transaction.objects.filter(user=demo_user, transaction_type='deposit').exists():
            Transaction.objects.create(
                user=demo_user,
                transaction_type='deposit',
                status='completed',
                amount=Decimal('0.05000000'),
                crypto_type='BTC',
                transaction_hash='a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
                to_address='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                from_address='1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                user_notes='Initial deposit'
            )
            print("✅ Created sample deposit transaction")
        
        # Sample pending withdrawal
        if not Transaction.objects.filter(user=demo_user, transaction_type='withdrawal').exists():
            Transaction.objects.create(
                user=demo_user,
                transaction_type='withdrawal',
                status='pending',
                amount=Decimal('500.00000000'),
                crypto_type='USDT',
                to_address='0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
                platform_fee=Decimal('10.00000000'),
                user_notes='Withdrawal to external wallet'
            )
            print("✅ Created sample withdrawal transaction")
        
    except User.DoesNotExist:
        print("⚠️  Demo user not found for sample transactions")
    except Exception as e:
        print(f"⚠️  Error creating sample transactions: {e}")
    
    print("\n🎉 Transaction System Setup Complete!")
    print("\n📝 System Summary:")
    print(f"   💰 Crypto Wallets: {CryptoWallet.objects.count()}")
    print(f"   👥 User Wallets: {UserWallet.objects.count()}")
    print(f"   📊 Transactions: {Transaction.objects.count()}")
    
    print("\n🌐 Available URLs:")
    print("   📊 Transactions: http://127.0.0.1:8000/transactions/")
    print("   💰 Deposit: http://127.0.0.1:8000/transactions/deposit/")
    print("   💸 Withdrawal: http://127.0.0.1:8000/transactions/withdrawal/")
    print("   👑 Admin Panel: http://127.0.0.1:8000/admin/")
    print("   🔧 Admin Transactions: http://127.0.0.1:8000/transactions/admin/")
    
    print("\n🔑 Demo Credentials:")
    print("   Username: demo")
    print("   Password: demo123")
    
    print("\n💡 Features Available:")
    print("   ✅ Crypto deposit system with proof upload")
    print("   ✅ Withdrawal request system with admin approval")
    print("   ✅ Transaction history and filtering")
    print("   ✅ Admin approval workflow")
    print("   ✅ Multiple cryptocurrency support")
    print("   ✅ Fee calculation system")
    print("   ✅ Email notifications")
    print("   ✅ Security features (address confirmation)")
    
    print("\n🚀 Ready to use! Start the server with: python manage.py runserver")

if __name__ == '__main__':
    main()
