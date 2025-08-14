import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("🧪 Testing Template Fixes...")

# Create test client
client = Client()

# Test 1: Check template structure
print("\n1️⃣ Checking template structure:")
dashboard_templates = [
    'templates/dashboard/base_dashboard.html',
    'templates/dashboard/dashboard.html',
    'templates/dashboard/deposit.html',
    'templates/dashboard/investment_detail.html',
    'templates/dashboard/investments.html',
    'templates/dashboard/portfolio.html',
    'templates/dashboard/support.html',
    'templates/dashboard/transactions.html',
    'templates/dashboard/withdraw.html'
]

for template_file in dashboard_templates:
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if it properly extends base template
        if 'extends \'dashboard/base_dashboard.html\'' in content:
            print(f"   ✅ {template_file} - Properly extends base template")
        elif template_file.endswith('base_dashboard.html'):
            print(f"   ✅ {template_file} - Base template (no extension needed)")
        else:
            print(f"   ❌ {template_file} - Does not extend base template")
        
        # Check for {% load static %}
        if '{% load static %}' in content:
            print(f"   ✅ {template_file} - Has {% load static %}")
        elif template_file.endswith('base_dashboard.html'):
            print(f"   ✅ {template_file} - Base template (static loaded)")
        else:
            print(f"   ⚠️  {template_file} - Missing {% load static %}")
        
        # Check for proper static file references
        if 'src="{% static' in content or 'href="{% static' in content:
            print(f"   ✅ {template_file} - Uses proper static file syntax")
        elif '../css/' in content or '../js/' in content:
            print(f"   ❌ {template_file} - Uses old relative paths")
        else:
            print(f"   ℹ️  {template_file} - No static files referenced")
    else:
        print(f"   ❌ {template_file} - File not found")
    print()

# Test 2: Test template rendering
print("\n2️⃣ Testing template rendering:")
try:
    # Try to login as demo user
    demo_user = User.objects.get(username='demo')
    login_success = client.login(username='demo', password='demo123')
    print(f"   Login successful: {login_success}")
    
    if login_success:
        # Test dashboard pages
        test_urls = [
            ('/dashboard/', 'Dashboard'),
            ('/investments/', 'Investments'),
            ('/portfolio/', 'Portfolio'),
            ('/transactions/', 'Transactions'),
        ]
        
        for url, name in test_urls:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"   ✅ {name} page: {response.status_code}")
                else:
                    print(f"   ❌ {name} page: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {name} page: Error - {e}")
    
except User.DoesNotExist:
    print("   ⚠️  Demo user not found")
except Exception as e:
    print(f"   ❌ Error testing templates: {e}")

# Test 3: Check for common template issues
print("\n3️⃣ Checking for common template issues:")

issues_found = []

for template_file in dashboard_templates:
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for duplicate HTML structure
        if content.count('<!DOCTYPE html>') > 0 and not template_file.endswith('base_dashboard.html'):
            issues_found.append(f"{template_file}: Contains duplicate HTML structure")
        
        # Check for duplicate navigation
        if content.count('<nav class="sidebar-nav">') > 0:
            issues_found.append(f"{template_file}: Contains duplicate sidebar navigation")
        
        # Check for duplicate top navigation
        if content.count('<nav class="top-nav">') > 0:
            issues_found.append(f"{template_file}: Contains duplicate top navigation")
        
        # Check for old static file references
        if '../css/' in content or '../js/' in content:
            issues_found.append(f"{template_file}: Uses old relative static file paths")

if issues_found:
    print("   Issues found:")
    for issue in issues_found:
        print(f"   ❌ {issue}")
else:
    print("   ✅ No common template issues found!")

print("\n📊 Template Fix Summary:")
print(f"   Total dashboard templates: {len(dashboard_templates)}")
print(f"   Templates checked: {len([t for t in dashboard_templates if os.path.exists(t)])}")
print(f"   Issues found: {len(issues_found)}")

print("\n🌐 URLs to test:")
print("   📊 Dashboard: http://127.0.0.1:8000/dashboard/")
print("   💰 Investments: http://127.0.0.1:8000/investments/")
print("   📈 Portfolio: http://127.0.0.1:8000/portfolio/")
print("   📋 Transactions: http://127.0.0.1:8000/transactions/")

print("\n🚀 Next steps:")
print("   1. Start server: python manage.py runserver")
print("   2. Login as demo user (demo/demo123)")
print("   3. Test all dashboard pages")
print("   4. Check that static files load correctly")

print("\n✅ Template fix testing completed!")
