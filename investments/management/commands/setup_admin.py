from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin user for the investment platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Admin username',
            default='admin'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email',
            default='admin@pipsmade.com'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password',
            default='admin123'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        # Check if admin user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists!')
            )
            return
        
        # Create superuser
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user!')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(
            self.style.SUCCESS(f'\nYou can now access the admin panel at /admin/')
        )
