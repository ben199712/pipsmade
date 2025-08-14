import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse

print("🔍 Debugging Template and URL Issues...")

# Check current working directory
print(f"\n📁 Current working directory: {os.getcwd()}")

# Check BASE_DIR
print(f"📁 Django BASE_DIR: {settings.BASE_DIR}")

# Check template directories
print(f"\n📂 Template directories:")
for template_config in settings.TEMPLATES:
    for template_dir in template_config['DIRS']:
        print(f"  • {template_dir}")
        if os.path.exists(template_dir):
            print(f"    ✅ Directory exists")
            dashboard_dir = os.path.join(template_dir, 'dashboard')
            if os.path.exists(dashboard_dir):
                print(f"    ✅ dashboard/ subdirectory exists")
                dashboard_template = os.path.join(dashboard_dir, 'dashboard.html')
                if os.path.exists(dashboard_template):
                    print(f"    ✅ dashboard.html template exists")
                else:
                    print(f"    ❌ dashboard.html template NOT found")
            else:
                print(f"    ❌ dashboard/ subdirectory NOT found")
        else:
            print(f"    ❌ Directory does not exist")

# Check if we can load the template
print(f"\n🔧 Testing template loading:")
try:
    template = get_template('dashboard/dashboard.html')
    print("✅ Template 'dashboard/dashboard.html' loaded successfully")
except Exception as e:
    print(f"❌ Error loading template: {e}")

# Check URL reverse
print(f"\n🔗 Testing URL reverse:")
try:
    dashboard_url = reverse('dashboard')
    print(f"✅ Dashboard URL: {dashboard_url}")
except Exception as e:
    print(f"❌ Error reversing 'dashboard' URL: {e}")

# List all available URLs
print(f"\n📋 Available URL patterns:")
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(f"  • {pattern}")

print(f"\n🚀 Debug complete!")
