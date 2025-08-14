import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("🧪 Testing Signup Fix...")

# Create a test client
client = Client()

# Test 1: Access signup page
print("\n1️⃣ Testing signup page access:")
try:
    response = client.get('/signup/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Signup page loads successfully!")
        # Check if the problematic JavaScript is fixed
        content = response.content.decode('utf-8')
        if 'dashboard/dashboard.html' in content:
            print("   ⚠️  Still contains problematic redirect")
        else:
            print("   ✅ JavaScript redirect fixed!")
    else:
        print(f"   ❌ Signup page error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Test signup form submission
print("\n2️⃣ Testing signup form submission:")
try:
    signup_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    response = client.post('/signup/', signup_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 302:
        print(f"   ✅ Redirected to: {response.url}")
        if '/dashboard/' in response.url:
            print("   ✅ Correct redirect to dashboard!")
        else:
            print(f"   ⚠️  Unexpected redirect: {response.url}")
    elif response.status_code == 200:
        print("   ⚠️  Form returned to signup page (check for validation errors)")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check URL patterns
print("\n3️⃣ Testing URL patterns:")
try:
    signup_url = reverse('signup')
    dashboard_url = reverse('dashboard')
    print(f"   Signup URL: {signup_url}")
    print(f"   Dashboard URL: {dashboard_url}")
    print("   ✅ URL patterns working!")
except Exception as e:
    print(f"   ❌ URL Error: {e}")

print("\n🚀 Test complete!")
print("\n💡 The fix should resolve the 'signup/dashboard/dashboard.html' error.")
print("   Now the signup form will properly submit to Django instead of using JavaScript redirect.")
