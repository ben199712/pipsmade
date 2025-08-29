#!/usr/bin/env python3
"""
Railway Email Setup Helper Script
This script helps you configure email settings for Railway deployment
"""

import os
import secrets
import string

def generate_secret_key():
    """Generate a secure Django secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def main():
    print("🚂 Railway Email Configuration Helper")
    print("=" * 50)
    
    print("\n📧 Email Configuration")
    print("-" * 30)
    
    # Get email configuration
    gmail_address = input("Enter your Gmail address: ").strip()
    gmail_app_password = input("Enter your Gmail app password (16 characters): ").strip()
    admin_email = input("Enter admin email for notifications: ").strip()
    
    # Generate Django secret key
    secret_key = generate_secret_key()
    
    print("\n🔑 Generated Django Secret Key")
    print("-" * 30)
    print(f"SECRET_KEY={secret_key}")
    
    print("\n📋 Environment Variables for Railway")
    print("-" * 40)
    print("Copy these to your Railway project environment variables:")
    print()
    
    env_vars = {
        'EMAIL_HOST_USER': gmail_address,
        'EMAIL_HOST_PASSWORD': gmail_app_password,
        'DEFAULT_FROM_EMAIL': 'support@pipsmade.com',
        'SUPPORT_EMAIL': 'support@pipsmade.com',
        'ADMIN_EMAIL': admin_email,
        'SITE_URL': 'https://pipsmade.com',
        'RAILWAY': 'true',
        'SECRET_KEY': secret_key,
    }
    
    for key, value in env_vars.items():
        print(f"{key}={value}")
    
    print("\n📝 Instructions:")
    print("1. Go to your Railway project dashboard")
    print("2. Click on 'Variables' tab")
    print("3. Add each environment variable above")
    print("4. Redeploy your application")
    print("5. Test with: python manage.py test_email --email your_email@gmail.com")
    
    print("\n⚠️  Important Notes:")
    print("- Keep your Gmail app password secure")
    print("- Never commit these values to git")
    print("- The SECRET_KEY should be unique for each deployment")
    print("- Make sure 2FA is enabled on your Gmail account")
    
    # Save to file (optional)
    save_to_file = input("\n💾 Save to .env file for reference? (y/n): ").strip().lower()
    if save_to_file == 'y':
        with open('railway.env', 'w') as f:
            f.write("# Railway Environment Variables\n")
            f.write("# DO NOT COMMIT THIS FILE TO GIT\n\n")
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        print("✅ Saved to railway.env (DO NOT COMMIT TO GIT)")
    
    print("\n🎉 Setup complete! Follow the instructions above to configure Railway.")

if __name__ == "__main__":
    main()
