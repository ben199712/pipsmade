from django.core.management.base import BaseCommand
from transactions.models import CryptoWallet

class Command(BaseCommand):
    help = 'Set up crypto wallet addresses for deposits'

    def handle(self, *args, **options):
        # Clear existing wallets
        CryptoWallet.objects.all().delete()
        
        # Sample wallet addresses (these should be real addresses in production)
        wallets_data = [
            {
                'crypto_type': 'BTC',
                'wallet_address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                'network': 'Bitcoin Network',
                'minimum_deposit': 0.001,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 2.00,
            },
            {
                'crypto_type': 'ETH',
                'wallet_address': '0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
                'network': 'ERC-20',
                'minimum_deposit': 0.01,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 2.50,
            },
            {
                'crypto_type': 'USDT',
                'wallet_address': '0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
                'network': 'ERC-20',
                'minimum_deposit': 10.00,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 1.50,
            },
            {
                'crypto_type': 'BNB',
                'wallet_address': '0x742d35Cc6634C0532925a3b8D4C9db96590c6C87',
                'network': 'BEP-20',
                'minimum_deposit': 0.1,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 2.00,
            },
            {
                'crypto_type': 'ADA',
                'wallet_address': 'addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj0vs2qd4a6gtmk4l3zcsr4qgqz',
                'network': 'Cardano Network',
                'minimum_deposit': 10.00,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 1.00,
            },
            {
                'crypto_type': 'LTC',
                'wallet_address': 'LTC1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
                'network': 'Litecoin Network',
                'minimum_deposit': 0.1,
                'deposit_fee_percentage': 0.00,
                'withdrawal_fee_percentage': 1.50,
            },
        ]
        
        created_count = 0
        for wallet_data in wallets_data:
            wallet, created = CryptoWallet.objects.get_or_create(
                crypto_type=wallet_data['crypto_type'],
                defaults=wallet_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created wallet: {wallet.get_crypto_type_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Wallet already exists: {wallet.get_crypto_type_display()}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} crypto wallets!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total wallets in database: {CryptoWallet.objects.count()}')
        )
        
        # Display wallet information
        self.stdout.write('\n📋 Available Crypto Wallets:')
        for wallet in CryptoWallet.objects.all():
            self.stdout.write(f'  • {wallet.get_crypto_type_display()} ({wallet.network})')
            self.stdout.write(f'    Address: {wallet.wallet_address}')
            self.stdout.write(f'    Min Deposit: {wallet.minimum_deposit} {wallet.crypto_type}')
            self.stdout.write(f'    Withdrawal Fee: {wallet.withdrawal_fee_percentage}%')
            self.stdout.write('')
