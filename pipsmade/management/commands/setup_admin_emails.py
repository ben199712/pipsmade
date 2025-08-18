from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pipsmade.models import AdminEmailConfig

class Command(BaseCommand):
    help = 'Set up admin email configuration for notifications'

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
            help='Admin email for notifications',
            default='admin@pipsmade.com'
        )
        parser.add_argument(
            '--notify-login',
            action='store_true',
            help='Enable login notifications',
            default=True
        )
        parser.add_argument(
            '--notify-signup',
            action='store_true',
            help='Enable signup notifications',
            default=True
        )
        parser.add_argument(
            '--notify-deposits',
            action='store_true',
            help='Enable deposit notifications',
            default=True
        )
        parser.add_argument(
            '--notify-withdrawals',
            action='store_true',
            help='Enable withdrawal notifications',
            default=True
        )
        parser.add_argument(
            '--notify-support',
            action='store_true',
            help='Enable support notifications',
            default=True
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        
        try:
            # Check if admin user exists
            try:
                admin_user = User.objects.get(username=username)
                if not admin_user.is_staff:
                    self.stdout.write(
                        self.style.ERROR(f'User "{username}" exists but is not a staff member!')
                    )
                    return
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Admin user "{username}" does not exist!')
                )
                self.stdout.write('Please create the admin user first using:')
                self.stdout.write(f'python manage.py createsuperuser --username {username}')
                return
            
            # Check if email config already exists
            if AdminEmailConfig.objects.filter(admin_user=admin_user).exists():
                self.stdout.write(
                    self.style.WARNING(f'Email configuration already exists for user "{username}"')
                )
                
                # Update existing config
                config = AdminEmailConfig.objects.get(admin_user=admin_user)
                config.email_address = email
                config.notify_login = options['notify_login']
                config.notify_signup = options['notify_signup']
                config.notify_deposits = options['notify_deposits']
                config.notify_withdrawals = options['notify_withdrawals']
                config.notify_support = options['notify_support']
                config.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Updated email configuration for user "{username}"')
                )
            else:
                # Create new config
                config = AdminEmailConfig.objects.create(
                    admin_user=admin_user,
                    email_address=email,
                    notify_login=options['notify_login'],
                    notify_signup=options['notify_signup'],
                    notify_deposits=options['notify_deposits'],
                    notify_withdrawals=options['notify_withdrawals'],
                    notify_support=options['notify_support']
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created email configuration for user "{username}"')
                )
            
            # Show configuration details
            self.stdout.write('\n📧 Email Configuration Details:')
            self.stdout.write(f'   Admin User: {username}')
            self.stdout.write(f'   Email Address: {email}')
            self.stdout.write(f'   Login Notifications: {"✅" if options["notify_login"] else "❌"}')
            self.stdout.write(f'   Signup Notifications: {"✅" if options["notify_signup"] else "❌"}')
            self.stdout.write(f'   Deposit Notifications: {"✅" if options["notify_deposits"] else "❌"}')
            self.stdout.write(f'   Withdrawal Notifications: {"✅" if options["notify_withdrawals"] else "❌"}')
            self.stdout.write(f'   Support Notifications: {"✅" if options["notify_support"] else "❌"}')
            
            self.stdout.write('\n🔧 Next Steps:')
            self.stdout.write('1. Go to Django admin: /admin/')
            self.stdout.write('2. Navigate to "Admin Email Configurations"')
            self.stdout.write('3. Edit the configuration if needed')
            self.stdout.write('4. Test email functionality using: python manage.py test_email')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up admin email configuration: {str(e)}')
            ) 