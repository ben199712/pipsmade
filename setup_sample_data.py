#!/usr/bin/env python
"""
Script to set up sample data for the investment platform
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

def main():
    print("🚀 Setting up sample data for pipsmade investment platform...")
    
    # 1. Create sample investment plans
    print("\n📊 Creating sample investment plans...")
    call_command('create_sample_plans')
    
    # 2. Create a test user if it doesn't exist
    print("\n👤 Setting up test user...")
    username = 'demo'
    try:
        user = User.objects.get(username=username)
        print(f"✅ Test user '{username}' already exists")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email='demo@pipsmade.com',
            password='demo123',
            first_name='Demo',
            last_name='User'
        )
        print(f"✅ Created test user: {username} (password: demo123)")
    
    # 3. Create sample investments for the test user
    print(f"\n💰 Creating sample investments for user '{username}'...")
    call_command('create_sample_investments', username=username, count=8)
    
    print("\n🎉 Sample data setup complete!")
    print("\n📝 You can now:")
    print(f"   1. Login with username: {username}, password: demo123")
    print("   2. View the investment plans")
    print("   3. Create new investments")
    print("   4. Check the portfolio dashboard")
    print("\n🔗 Start the server with: python manage.py runserver")

if __name__ == '__main__':
    main()
