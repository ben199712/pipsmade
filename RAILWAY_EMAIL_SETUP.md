# 📧 Email Setup Guide for Railway.com with Custom Domain

## 🚨 **Current Issue**
Your email notifications stopped working after adding a custom domain to Railway.com. This is because:
1. The domain change affected environment detection
2. Email configuration conflicts between local and production settings
3. Missing or incorrect environment variables on Railway

## 🔧 **Step-by-Step Fix**

### **Step 1: Setup Gmail App Password**

1. **Go to Google Account Settings:**
   - Visit: https://myaccount.google.com/
   - Click "Security" in the left sidebar

2. **Enable 2-Factor Authentication:**
   - Under "Signing in to Google", click "2-Step Verification"
   - Follow the setup process if not already enabled

3. **Generate App Password:**
   - Go back to Security settings
   - Click "App passwords" (under 2-Step Verification)
   - Select "Mail" as the app
   - Select "Other" as the device and enter "Railway PipsMade"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### **Step 2: Set Railway Environment Variables**

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app/dashboard
   - Select your PipsMade project

2. **Add Environment Variables:**
   - Click on your service/project
   - Go to "Variables" tab
   - Add these variables:

```bash
EMAIL_HOST_USER=Celewizzy106@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
ADMIN_EMAIL=Celewizzy106@gmail.com
DEFAULT_FROM_EMAIL=support@pipsmade.com
RAILWAY_ENVIRONMENT_NAME=production
CUSTOM_DOMAIN=pipsmade.com
```

**🚨 CRITICAL: Use your actual Gmail app password, not the example above!**

### **Step 2b: Quick Setup with Railway CLI (Optional)**

If you have Railway CLI installed:

```bash
# Make the script executable
chmod +x railway_setup_email.sh

# Run the setup script
./railway_setup_email.sh
```

This will automatically set most variables, but you still need to set `EMAIL_HOST_PASSWORD` manually.

### **Step 3: Deploy and Test**

1. **Redeploy your application:**
   - Railway will automatically redeploy when you add environment variables
   - Or manually trigger a deployment

2. **Test email functionality with domain:**
   ```bash
   # Test domain-specific email configuration
   railway run python test_railway_domain_email.py

   # Test with management command
   railway run python manage.py test_email --email your-email@gmail.com
   ```

3. **Check logs:**
   ```bash
   railway logs --tail
   ```

4. **Verify domain configuration:**
   ```bash
   # Check if your domain is properly configured
   railway domains

   # Check environment variables
   railway variables
   ```

## 🧪 **Testing Commands**

### **Test Email Configuration:**
```bash
python manage.py test_email --config
```

### **Test Email Connection:**
```bash
python manage.py test_email --test-connection
```

### **Send Test Email:**
```bash
python manage.py test_email --email your-email@gmail.com
```

## 🔍 **Troubleshooting**

### **Common Issues:**

#### **1. "Authentication failed" Error**
- **Cause:** Wrong app password or 2FA not enabled
- **Fix:** 
  - Regenerate Gmail app password
  - Ensure 2FA is enabled
  - Use app password, not regular password

#### **2. "Connection timed out" Error**
- **Cause:** Railway blocking SMTP connections
- **Fix:** 
  - Try alternative email services (SendGrid, Mailgun)
  - Check Railway firewall settings

#### **3. "Environment variables not found" Error**
- **Cause:** Variables not set in Railway
- **Fix:** 
  - Double-check variable names (case-sensitive)
  - Ensure variables are set in correct service
  - Redeploy after adding variables

#### **4. "Email sent but not received" Error**
- **Cause:** Gmail spam filters or rate limiting
- **Fix:** 
  - Check spam folder
  - Verify recipient email address
  - Try different recipient

### **Alternative Email Services (Recommended for Production):**

#### **SendGrid (Recommended):**
```bash
# Railway Environment Variables
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

#### **Mailgun:**
```bash
# Railway Environment Variables
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-mailgun-username
EMAIL_HOST_PASSWORD=your-mailgun-password
```

## 📋 **Verification Checklist**

- [ ] Gmail 2FA enabled
- [ ] Gmail app password generated
- [ ] Railway environment variables set
- [ ] Application redeployed
- [ ] Test email sent successfully
- [ ] Email received in inbox
- [ ] Login notifications working
- [ ] Signup notifications working
- [ ] Deposit notifications working
- [ ] Withdrawal notifications working

## 🚀 **Quick Fix Commands**

### **1. Check Current Configuration:**
```bash
railway run python manage.py test_email --config
```

### **2. Test Email System:**
```bash
railway run python manage.py test_email --email your-email@gmail.com
```

### **3. Check Application Logs:**
```bash
railway logs --tail
```

### **4. Restart Application:**
```bash
railway up --detach
```

## 📞 **Support**

If you're still having issues:

1. **Check Railway Logs:**
   ```bash
   railway logs | grep -i email
   ```

2. **Test Locally First:**
   - Set same environment variables locally
   - Test with `python manage.py test_email`
   - Ensure it works locally before deploying

3. **Contact Railway Support:**
   - Some hosting providers block SMTP
   - Railway support can confirm if SMTP is blocked

## 🎯 **Expected Result**

After following this guide:
- ✅ Email notifications will work on Railway.com
- ✅ Admin will receive login notifications
- ✅ Admin will receive signup notifications  
- ✅ Admin will receive deposit notifications
- ✅ Admin will receive withdrawal notifications
- ✅ All emails will be properly formatted and delivered

## 🔄 **Next Steps**

1. **Follow Step 1-3 above**
2. **Test with the provided commands**
3. **Verify notifications are working**
4. **Consider upgrading to professional email service for production**

The enhanced email system I've created includes multiple fallback methods and better error handling specifically for Railway.com deployment!
