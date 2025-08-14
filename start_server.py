#!/usr/bin/env python
"""
Simple script to start the pipsmade investment platform server
"""
import os
import sys
import django
import subprocess

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User
from investments.models import InvestmentPlan

def check_system():
    print("🔍 Checking system status...")
    
    # Check if investment plans exist
    plans_count = InvestmentPlan.objects.count()
    print(f"📊 Investment plans: {plans_count}")
    
    # Check if demo user exists
    try:
        demo_user = User.objects.get(username='demo')
        print(f"👤 Demo user: ✅ {demo_user.username}")
    except User.DoesNotExist:
        print("👤 Demo user: ❌ Not found")
        print("   Run: python create_demo_user.py")
    
    # Check if admin user exists
    admin_users = User.objects.filter(is_superuser=True).count()
    print(f"👑 Admin users: {admin_users}")
    
    return plans_count > 0

def main():
    print("🚀 Starting pipsmade Investment Platform...")
    
    # Check system
    system_ready = check_system()
    
    if not system_ready:
        print("\n⚠️  System not fully set up. Run these commands first:")
        print("   python create_plans_simple.py")
        print("   python create_demo_user.py")
        print("   python create_admin.py")
        return
    
    print("\n✅ System ready!")
    print("\n📝 Available URLs:")
    print("   🏠 Home: http://127.0.0.1:8000/")
    print("   🔐 Login: http://127.0.0.1:8000/login/")
    print("   📊 Dashboard: http://127.0.0.1:8000/dashboard/")
    print("   💰 Investments: http://127.0.0.1:8000/investments/")
    print("   👑 Admin: http://127.0.0.1:8000/admin/")
    
    print("\n🔑 Demo Credentials:")
    print("   Username: demo")
    print("   Password: demo123")
    
    print("\n🚀 Starting development server...")
    print("   Press Ctrl+C to stop the server")
    print("   If you get template errors, make sure you're using the correct URLs above")
    
    # Start the server
    try:
        subprocess.run(['python', 'manage.py', 'runserver', '127.0.0.1:8000'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTry running manually: python manage.py runserver")

if __name__ == '__main__':
    main()
