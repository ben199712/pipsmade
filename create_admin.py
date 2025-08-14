import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipsmade.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user
username = 'admin'
email = 'admin@pipsmade.com'
password = 'admin123'

try:
    admin_user = User.objects.get(username=username)
    print(f'✅ Admin user "{username}" already exists')
except User.DoesNotExist:
    admin_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f'✅ Created admin user!')
    print(f'   Username: {username}')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
    print(f'\n🔗 Access admin panel at: http://127.0.0.1:8000/admin/')

print(f'\n🚀 Admin credentials:')
print(f'   Username: {username}')
print(f'   Password: {password}')
