import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from transactions.models import Transaction

print("🧪 Testing Admin Interface...")

# Create test client
client = Client()

# Test 1: Check admin page accessibility
print("\n1️⃣ Testing admin page access:")
try:
    response = client.get('/transactions/admin/')
    print(f"   Admin page status: {response.status_code}")
    
    if response.status_code == 302:
        print("   ✅ Redirects to login (expected for non-authenticated user)")
    elif response.status_code == 200:
        print("   ✅ Page loads successfully")
    else:
        print(f"   ⚠️  Unexpected status code: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ Error accessing admin page: {e}")

# Test 2: Check transaction methods
print("\n2️⃣ Testing transaction helper methods:")
transactions = Transaction.objects.all()

for transaction in transactions:
    print(f"\nTransaction #{transaction.id}:")
    print(f"  Type: {transaction.transaction_type}")
    print(f"  Status: {transaction.status}")
    
    try:
        has_deposit = transaction.has_deposit_request()
        has_withdrawal = transaction.has_withdrawal_request()
        print(f"  Has deposit request: {has_deposit}")
        print(f"  Has withdrawal request: {has_withdrawal}")
        
        if transaction.transaction_type == 'deposit' and has_deposit:
            print(f"  Deposit request ID: {transaction.deposit_request.id}")
        elif transaction.transaction_type == 'withdrawal' and has_withdrawal:
            print(f"  Withdrawal request ID: {transaction.withdrawal_request.id}")
            
    except Exception as e:
        print(f"  ❌ Error checking requests: {e}")

# Test 3: Check if we can create admin user
print("\n3️⃣ Checking admin user setup:")
try:
    admin_users = User.objects.filter(is_superuser=True)
    print(f"   Admin users found: {admin_users.count()}")
    
    if admin_users.count() == 0:
        print("   💡 No admin users found. Create one with:")
        print("      python manage.py createsuperuser")
    else:
        for admin in admin_users:
            print(f"   ✅ Admin user: {admin.username}")
            
except Exception as e:
    print(f"   ❌ Error checking admin users: {e}")

print("\n📊 System Status:")
print(f"   Total transactions: {Transaction.objects.count()}")
print(f"   Pending transactions: {Transaction.objects.filter(status='pending').count()}")

print("\n🌐 URLs to test:")
print("   📊 Admin Dashboard: http://127.0.0.1:8000/transactions/admin/")
print("   🔧 Django Admin: http://127.0.0.1:8000/admin/")

print("\n🚀 Next steps:")
print("   1. Start server: python manage.py runserver")
print("   2. Create admin user if needed: python manage.py createsuperuser")
print("   3. Login and test admin interface")

print("\n✅ Admin interface test completed!")
