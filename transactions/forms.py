from django import forms
from decimal import Decimal
from .models import CryptoWallet, UserWallet, DepositRequest, WithdrawalRequest

class DepositForm(forms.Form):
    """Form for crypto deposit requests"""
    crypto_wallet = forms.ModelChoiceField(
        queryset=CryptoWallet.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'cryptoWallet'
        }),
        empty_label="Select Cryptocurrency"
    )
    
    amount = forms.DecimalField(
        max_digits=18,
        decimal_places=8,
        min_value=Decimal('0.00000001'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to deposit',
            'step': '0.00000001',
            'id': 'depositAmount'
        })
    )
    
    transaction_hash = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter blockchain transaction hash',
            'id': 'transactionHash'
        }),
        help_text="The transaction hash from your wallet/exchange"
    )
    
    sender_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the address you sent from',
            'id': 'senderAddress'
        }),
        help_text="The wallet address you sent the crypto from"
    )
    
    proof_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'proofImage'
        }),
        help_text="Optional: Upload screenshot of transaction (recommended)"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        crypto_wallet = cleaned_data.get('crypto_wallet')
        amount = cleaned_data.get('amount')
        
        if crypto_wallet and amount:
            if amount < crypto_wallet.minimum_deposit:
                raise forms.ValidationError(
                    f'Minimum deposit for {crypto_wallet.crypto_type} is {crypto_wallet.minimum_deposit}'
                )
        
        return cleaned_data

class WithdrawalForm(forms.Form):
    """Form for crypto withdrawal requests"""
    crypto_type = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'cryptoType'
        })
    )
    
    amount = forms.DecimalField(
        max_digits=18,
        decimal_places=8,
        min_value=Decimal('0.00000001'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to withdraw',
            'step': '0.00000001',
            'id': 'withdrawAmount'
        })
    )
    
    destination_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter destination wallet address',
            'id': 'destinationAddress'
        }),
        help_text="The wallet address to send crypto to"
    )
    
    network = forms.ChoiceField(
        choices=[
            ('ERC-20', 'Ethereum (ERC-20)'),
            ('BEP-20', 'Binance Smart Chain (BEP-20)'),
            ('TRC-20', 'Tron (TRC-20)'),
            ('BTC', 'Bitcoin Network'),
            ('LTC', 'Litecoin Network'),
            ('ADA', 'Cardano Network'),
            ('DOT', 'Polkadot Network'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'network'
        }),
        help_text="Select the network to send on"
    )
    
    confirm_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm destination address',
            'id': 'confirmAddress'
        }),
        help_text="Re-enter the destination address to confirm"
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Get user's available crypto balances
            user_wallets = UserWallet.objects.filter(user=user, balance__gt=0)
            choices = [(wallet.crypto_type, f"{wallet.crypto_type} (Balance: {wallet.balance})") 
                      for wallet in user_wallets]
            self.fields['crypto_type'].choices = choices
    
    def clean(self):
        cleaned_data = super().clean()
        destination_address = cleaned_data.get('destination_address')
        confirm_address = cleaned_data.get('confirm_address')
        
        if destination_address and confirm_address:
            if destination_address != confirm_address:
                raise forms.ValidationError("Destination addresses do not match!")
        
        return cleaned_data

class AdminWalletForm(forms.ModelForm):
    """Form for admin to manage crypto wallets"""
    class Meta:
        model = CryptoWallet
        fields = [
            'crypto_type', 'wallet_address', 'network', 'is_active',
            'minimum_deposit', 'deposit_fee_percentage', 'withdrawal_fee_percentage'
        ]
        widgets = {
            'crypto_type': forms.Select(attrs={'class': 'form-select'}),
            'wallet_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter wallet address'
            }),
            'network': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., ERC-20, BEP-20, TRC-20'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'minimum_deposit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00000001'
            }),
            'deposit_fee_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'withdrawal_fee_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }

class TransactionSearchForm(forms.Form):
    """Form for searching transactions"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by username, email, or transaction hash'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + list(CryptoWallet.objects.model._meta.get_field('crypto_type').choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    transaction_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + [
            ('deposit', 'Deposit'),
            ('withdrawal', 'Withdrawal'),
            ('investment', 'Investment'),
            ('profit', 'Profit'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
