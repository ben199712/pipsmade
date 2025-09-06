#!/bin/bash

# Railway.com Email Setup Script
# This script helps set up email environment variables for Railway deployment

echo "🚂 Railway.com Email Setup Script"
echo "=================================="

echo ""
echo "This script will help you set up email environment variables for Railway.com"
echo "Make sure you have the Railway CLI installed and are logged in."
echo ""

# Check if railway CLI is available
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "   Install it from: https://railway.app/cli"
    echo "   Or run: npm install -g @railway/cli"
    exit 1
fi

echo "✅ Railway CLI found"

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway"
    echo "   Run: railway login"
    exit 1
fi

echo "✅ Logged in to Railway"

# Get current project info
echo ""
echo "📋 Current Railway Project:"
railway status

echo ""
echo "🔧 Setting up email environment variables..."
echo ""

# Set email environment variables
echo "Setting EMAIL_HOST_USER..."
railway variables set EMAIL_HOST_USER=Celewizzy106@gmail.com

echo "Setting EMAIL_HOST_PASSWORD..."
echo "⚠️  You need to set your Gmail App Password manually:"
echo "   1. Go to Google Account > Security > 2-Step Verification > App passwords"
echo "   2. Generate an app password for 'Mail'"
echo "   3. Run: railway variables set EMAIL_HOST_PASSWORD=your-16-char-app-password"

echo ""
echo "Setting other email variables..."
railway variables set ADMIN_EMAIL=Celewizzy106@gmail.com
railway variables set DEFAULT_FROM_EMAIL=support@pipsmade.com
railway variables set SUPPORT_EMAIL=support@pipsmade.com

echo ""
echo "Setting Railway environment..."
railway variables set RAILWAY_ENVIRONMENT_NAME=production

echo ""
echo "Setting custom domain (if you have one)..."
read -p "Do you have a custom domain? (y/n): " has_domain
if [[ $has_domain == "y" || $has_domain == "Y" ]]; then
    read -p "Enter your custom domain (e.g., pipsmade.com): " custom_domain
    railway variables set CUSTOM_DOMAIN=$custom_domain
    echo "✅ Custom domain set: $custom_domain"
fi

echo ""
echo "📋 Current environment variables:"
railway variables

echo ""
echo "🚀 Deployment and Testing:"
echo "1. Your app will automatically redeploy with new variables"
echo "2. Test email functionality:"
echo "   railway run python test_railway_domain_email.py"
echo ""
echo "3. Check logs for any issues:"
echo "   railway logs --tail"
echo ""
echo "4. Test specific email functions:"
echo "   railway run python manage.py test_email --email your-email@gmail.com"

echo ""
echo "⚠️  IMPORTANT: Don't forget to set EMAIL_HOST_PASSWORD manually!"
echo "   Run: railway variables set EMAIL_HOST_PASSWORD=your-app-password"

echo ""
echo "✅ Email setup script completed!"
echo "   Your Railway app should now have proper email configuration."
