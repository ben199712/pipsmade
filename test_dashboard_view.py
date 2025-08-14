import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse

print("🧪 Testing Dashboard View...")

# Create a test client
client = Client()

# Test 1: Access dashboard without login (should redirect to login)
print("\n1️⃣ Testing dashboard access without login:")
try:
    response = client.get('/dashboard/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirected to: {response.url}")
    else:
        print(f"   Response: {response.content[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Login and access dashboard
print("\n2️⃣ Testing dashboard access with login:")
try:
    # Get or create demo user
    try:
        user = User.objects.get(username='demo')
    except User.DoesNotExist:
        user = User.objects.create_user('demo', 'demo@test.com', 'demo123')
    
    # Login
    login_success = client.login(username='demo', password='demo123')
    print(f"   Login successful: {login_success}")
    
    if login_success:
        # Access dashboard
        response = client.get('/dashboard/')
        print(f"   Dashboard status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard loaded successfully!")
        else:
            print(f"   ❌ Dashboard error: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"   Content preview: {response.content[:200]}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Test URL patterns
print("\n3️⃣ Testing URL patterns:")
try:
    dashboard_url = reverse('dashboard')
    print(f"   Dashboard URL: {dashboard_url}")
    
    login_url = reverse('login')
    print(f"   Login URL: {login_url}")
    
    investments_url = reverse('investments')
    print(f"   Investments URL: {investments_url}")
    
except Exception as e:
    print(f"   ❌ URL Error: {e}")

print("\n🚀 Test complete!")
print("\n💡 If you're getting the 'signup/dashboard/dashboard.html' error:")
print("   1. Make sure you're accessing the correct URL: http://127.0.0.1:8000/dashboard/")
print("   2. Not: http://127.0.0.1:8000/signup/dashboard/")
print("   3. Try logging in first at: http://127.0.0.1:8000/login/")
print("   4. Use demo/demo123 credentials")
