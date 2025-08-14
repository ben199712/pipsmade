# 🔧 Troubleshooting Guide - pipsmade Investment Platform

## Common Issues and Solutions

### ❌ Error: "signup/dashboard/dashboard.html does not exist"

**Problem**: Django is looking for templates in the wrong path.

**Possible Causes & Solutions**:

#### 1. **Wrong URL Access**
- ❌ **Don't access**: `http://127.0.0.1:8000/signup/dashboard/`
- ✅ **Correct URLs**:
  - Home: `http://127.0.0.1:8000/`
  - Login: `http://127.0.0.1:8000/login/`
  - Dashboard: `http://127.0.0.1:8000/dashboard/`
  - Investments: `http://127.0.0.1:8000/investments/`

#### 2. **Login Required**
The dashboard requires authentication. Always login first:
1. Go to: `http://127.0.0.1:8000/login/`
2. Use credentials: `demo` / `demo123`
3. You'll be redirected to the dashboard automatically

#### 3. **Template Path Issues**
If the error persists, check:
```bash
# Verify templates exist
ls templates/dashboard/
# Should show: base_dashboard.html, dashboard.html, investments.html, etc.

# Check Django settings
python manage.py check
```

### 🚀 Quick Setup Commands

If you're missing data or users:

```bash
# 1. Create investment plans
python create_plans_simple.py

# 2. Create demo user with sample investments
python create_demo_user.py

# 3. Create admin user (optional)
python create_admin.py

# 4. Start server
python start_server.py
```

### 🔍 System Check

Run this to verify everything is working:
```bash
python test_investment_system.py
```

### 📋 Correct Access Flow

1. **Start Server**:
   ```bash
   python manage.py runserver
   ```

2. **Access Home Page**:
   - URL: `http://127.0.0.1:8000/`
   - Should show the landing page with login/signup buttons

3. **Login**:
   - Click "Login" or go to: `http://127.0.0.1:8000/login/`
   - Use: `demo` / `demo123`

4. **Dashboard Access**:
   - After login, you'll be redirected to: `http://127.0.0.1:8000/dashboard/`
   - Should show portfolio metrics and recent investments

5. **Investments**:
   - Click "Investments" in sidebar or go to: `http://127.0.0.1:8000/investments/`
   - Should show investment plans and your active investments

### 🐛 Debug Steps

If you're still having issues:

1. **Check Django Version**:
   ```bash
   python -c "import django; print(django.VERSION)"
   ```

2. **Verify Database**:
   ```bash
   python manage.py migrate
   ```

3. **Check URL Patterns**:
   ```bash
   python manage.py show_urls  # If django-extensions installed
   # OR
   python debug_templates.py
   ```

4. **Template Debug**:
   ```bash
   python debug_templates.py
   ```

### 🔧 Manual Template Check

If templates are missing:
```bash
# Check if templates directory exists
ls templates/

# Should contain:
# - accounts/
# - dashboard/
# - base.html
# - index.html

# Check dashboard templates
ls templates/dashboard/

# Should contain:
# - base_dashboard.html
# - dashboard.html
# - investments.html
# - portfolio.html
```

### 📞 Still Having Issues?

1. **Check the exact error message** - copy the full traceback
2. **Verify the URL** you're trying to access
3. **Check browser developer tools** for any JavaScript errors
4. **Try incognito/private browsing** to rule out cache issues

### ✅ Expected Behavior

When everything is working correctly:
- ✅ Home page loads at `http://127.0.0.1:8000/`
- ✅ Login works with `demo`/`demo123`
- ✅ Dashboard shows portfolio metrics
- ✅ Investments page shows 6 investment plans
- ✅ Can create new investments
- ✅ Investment calculator works in modal

### 🎯 Quick Test

Run this one-liner to test everything:
```bash
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()
from django.template.loader import get_template
from django.urls import reverse
print('✅ Template:', get_template('dashboard/dashboard.html'))
print('✅ URL:', reverse('dashboard'))
print('✅ System working!')
"
```

If this runs without errors, your system is properly configured!
