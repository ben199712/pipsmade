from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db import models
from django.utils import timezone
from decimal import Decimal
from .models import (
    CryptoWallet, UserWallet, Transaction,
    DepositRequest, WithdrawalRequest, TransactionNotification
)
from .forms import DepositForm, WithdrawalForm
from .email_notifications import send_deposit_notification, send_withdrawal_notification

@login_required
def transactions_view(request):
    """Main transactions page showing history and options"""
    # Get user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')

    # Filter by type if specified
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    # Filter by status if specified
    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(status=status)

    # Pagination
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get available crypto wallets for deposits
    crypto_wallets = CryptoWallet.objects.filter(is_active=True)

    # Calculate totals
    total_deposits = transactions.filter(
        transaction_type='deposit',
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_withdrawals = transactions.filter(
        transaction_type='withdrawal',
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    pending_transactions = transactions.filter(status='pending').count()

    context = {
        'page_obj': page_obj,
        'crypto_wallets': crypto_wallets,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'pending_transactions': pending_transactions,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'status_choices': Transaction.STATUS_CHOICES,
        'current_type': transaction_type,
        'current_status': status,
    }

    return render(request, 'transactions/transactions.html', context)

@login_required
def deposit_view(request):
    """Crypto deposit page"""
    if request.method == 'POST':
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            crypto_wallet = form.cleaned_data['crypto_wallet']
            amount = form.cleaned_data['amount']
            transaction_hash = form.cleaned_data['transaction_hash']
            sender_address = form.cleaned_data['sender_address']
            proof_image = form.cleaned_data.get('proof_image')

            # Check minimum deposit
            if amount < crypto_wallet.minimum_deposit:
                messages.error(request, f'Minimum deposit for {crypto_wallet.crypto_type} is {crypto_wallet.minimum_deposit}')
                return redirect('deposit')

            # Create transaction
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                status='pending',
                amount=amount,
                crypto_type=crypto_wallet.crypto_type,
                transaction_hash=transaction_hash,
                to_address=crypto_wallet.wallet_address,
                from_address=sender_address,
                user_notes=f"Deposit via {crypto_wallet.network}"
            )

            # Create deposit request
            deposit_request = DepositRequest.objects.create(
                user=request.user,
                transaction=transaction,
                crypto_wallet=crypto_wallet,
                amount=amount,
                transaction_hash=transaction_hash,
                sender_address=sender_address,
                proof_image=proof_image
            )

            # Send admin notification email using the simple email system
            try:
                send_deposit_notification(deposit_request)
                print(f"Deposit notification sent successfully for user {request.user.username}")
            except Exception as e:
                # Log error but don't fail deposit request
                print(f"Failed to send deposit notification: {e}")

            messages.success(request, 'Deposit request submitted successfully! It will be reviewed by our team.')
            return redirect('transactions')
    else:
        form = DepositForm()

    crypto_wallets = CryptoWallet.objects.filter(is_active=True)

    context = {
        'form': form,
        'crypto_wallets': crypto_wallets,
    }

    return render(request, 'transactions/deposit.html', context)

@login_required
def withdrawal_view(request):
    """Crypto withdrawal page"""
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            crypto_type = form.cleaned_data['crypto_type']
            amount = form.cleaned_data['amount']
            destination_address = form.cleaned_data['destination_address']
            network = form.cleaned_data['network']

            # Get user's wallet balance
            try:
                user_wallet = UserWallet.objects.get(user=request.user, crypto_type=crypto_type)
            except UserWallet.DoesNotExist:
                messages.error(request, f'You do not have a {crypto_type} wallet.')
                return redirect('withdrawal')

            # Check if user has sufficient balance
            if user_wallet.balance < amount:
                messages.error(request, f'Insufficient {crypto_type} balance. Available: {user_wallet.balance}')
                return redirect('withdrawal')

            # Calculate fees
            crypto_wallet = CryptoWallet.objects.filter(crypto_type=crypto_type, is_active=True).first()
            if crypto_wallet:
                platform_fee = amount * (crypto_wallet.withdrawal_fee_percentage / 100)
            else:
                platform_fee = Decimal('0')

            # Create transaction
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='withdrawal',
                status='pending',
                amount=amount,
                crypto_type=crypto_type,
                to_address=destination_address,
                platform_fee=platform_fee,
                user_notes=f"Withdrawal via {network}"
            )

            # Create withdrawal request
            withdrawal_request = WithdrawalRequest.objects.create(
                user=request.user,
                transaction=transaction,
                crypto_type=crypto_type,
                amount=amount,
                destination_address=destination_address,
                network=network,
                platform_fee=platform_fee,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Send admin notification email using the simple email system
            try:
                send_withdrawal_notification(withdrawal_request)
                print(f"Withdrawal notification sent successfully for user {request.user.username}")
            except Exception as e:
                # Log error but don't fail withdrawal request
                print(f"Failed to send withdrawal notification: {e}")

            messages.success(request, 'Withdrawal request submitted successfully! It will be processed by our team.')
            return redirect('transactions')
    else:
        form = WithdrawalForm()

    # Get user's wallet balances for context
    user_wallets = UserWallet.objects.filter(user=request.user)
    
    # Calculate total available balance
    try:
        # Calculate crypto balance from user wallets
        total_crypto_balance = sum(wallet.balance for wallet in user_wallets)
        
        # Get portfolio data from investments
        from investments.models import UserPortfolio
        try:
            portfolio = UserPortfolio.objects.get(user=request.user)
            total_portfolio_value = portfolio.total_current_value or 0
        except UserPortfolio.DoesNotExist:
            total_portfolio_value = 0
        
        total_available_balance = total_crypto_balance + total_portfolio_value
    except Exception as e:
        print(f"Error calculating balances: {e}")
        total_crypto_balance = 0
        total_portfolio_value = 0
        total_available_balance = 0

    context = {
        'form': form,
        'user_wallets': user_wallets,
        'total_crypto_balance': total_crypto_balance,
        'total_portfolio_value': total_portfolio_value,
        'total_available_balance': total_available_balance,
        'total_balance': total_available_balance,  # For backward compatibility
        'total_withdrawals': Transaction.objects.filter(
            user=request.user,
            transaction_type='withdrawal',
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
        'pending_withdrawals': Transaction.objects.filter(
            user=request.user,
            transaction_type='withdrawal',
            status='pending'
        ).count(),
        'recent_withdrawals': Transaction.objects.filter(
            user=request.user,
            transaction_type='withdrawal'
        ).order_by('-created_at')[:5],
    }

    return render(request, 'dashboard/withdraw.html', context)

@login_required
def transaction_detail(request, transaction_id):
    """View detailed information about a specific transaction"""
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    context = {
        'transaction': transaction,
    }

    return render(request, 'transactions/transaction_detail.html', context)

# Admin Views
@staff_member_required
def admin_transactions(request):
    """Admin view for managing all transactions"""
    print(f"DEBUG: admin_transactions view called")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request GET params: {request.GET}")
    
    transactions = Transaction.objects.all().order_by('-created_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        transactions = transactions.filter(status=status)

    # Filter by type
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    # Search by user
    search = request.GET.get('search')
    if search:
        transactions = transactions.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(transaction_hash__icontains=search)
        )

    # Pagination
    paginator = Paginator(transactions, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    stats = {
        'pending_deposits': Transaction.objects.filter(transaction_type='deposit', status='pending').count(),
        'pending_withdrawals': Transaction.objects.filter(transaction_type='withdrawal', status='pending').count(),
        'total_volume_today': Transaction.objects.filter(
            created_at__date=timezone.now().date(),
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }

    print(f"DEBUG: Stats: {stats}")
    print(f"DEBUG: Transaction count: {transactions.count()}")
    print(f"DEBUG: Page count: {page_obj.paginator.num_pages}")

    context = {
        'page_obj': page_obj,
        'stats': stats,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'status_choices': Transaction.STATUS_CHOICES,
        'current_status': status,
        'current_type': transaction_type,
        'search_query': search,
    }

    print(f"DEBUG: Rendering admin_transactions template")
    return render(request, 'transactions/admin_transactions.html', context)

@staff_member_required
def admin_approve_deposit(request, deposit_id):
    """Admin approve deposit request"""
    print(f"DEBUG: admin_approve_deposit view called for deposit_id: {deposit_id}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request user: {request.user}")
    
    deposit_request = get_object_or_404(DepositRequest, id=deposit_id)
    transaction = deposit_request.transaction
    
    print(f"DEBUG: Found deposit_request: {deposit_request}")
    print(f"DEBUG: Found transaction: {transaction}")
    print(f"DEBUG: Transaction status: {transaction.status}")

    if request.method == 'POST':
        print(f"DEBUG: Processing deposit {deposit_id}")
        print(f"DEBUG: POST data: {request.POST}")
        
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')

        print(f"DEBUG: Action: {action}")
        print(f"DEBUG: Admin notes: {admin_notes}")
        print(f"DEBUG: Action type: {type(action)}")
        print(f"DEBUG: All POST keys: {list(request.POST.keys())}")

        if action == 'approve':
            print(f"DEBUG: Approving deposit {deposit_id}")
            # Update transaction status
            transaction.status = 'completed'
            transaction.approved_by = request.user
            transaction.approved_at = timezone.now()
            transaction.admin_notes = admin_notes
            transaction.save()

            # Update deposit request
            deposit_request.admin_verified = True
            deposit_request.verified_by = request.user
            deposit_request.verified_at = timezone.now()
            deposit_request.verification_notes = admin_notes
            deposit_request.save()

            # Update user wallet balance
            user_wallet, created = UserWallet.objects.get_or_create(
                user=transaction.user,
                crypto_type=transaction.crypto_type,
                defaults={'balance': 0}
            )
            user_wallet.balance += transaction.amount
            user_wallet.save()

            # Create notification
            TransactionNotification.objects.create(
                user=transaction.user,
                transaction=transaction,
                title='Deposit Confirmed',
                message=f'Your deposit of {transaction.amount} {transaction.crypto_type} has been confirmed.',
                notification_type='deposit_confirmed'
            )

            messages.success(request, f'Deposit approved and {transaction.amount} {transaction.crypto_type} added to user wallet.')
            print(f"DEBUG: Redirecting to admin_transactions")
            return redirect('admin_transactions')

        elif action == 'reject':
            print(f"DEBUG: Rejecting deposit {deposit_id}")
            transaction.status = 'rejected'
            transaction.approved_by = request.user
            transaction.approved_at = timezone.now()
            transaction.rejection_reason = admin_notes
            transaction.admin_notes = admin_notes
            transaction.save()

            deposit_request.verification_notes = admin_notes
            deposit_request.save()

            messages.warning(request, 'Deposit request rejected.')
            print(f"DEBUG: Redirecting to admin_transactions")
            return redirect('admin_transactions')
        else:
            print(f"DEBUG: Invalid action: {action}")
            print(f"DEBUG: Action type: {type(action)}")
            print(f"DEBUG: All POST keys: {list(request.POST.keys())}")
            messages.error(request, f'Invalid action: {action}')
            return redirect('admin_transactions')

    print(f"DEBUG: Rendering admin_approve_deposit template")
    context = {
        'deposit_request': deposit_request,
        'transaction': transaction,
    }

    return render(request, 'transactions/admin_approve_deposit.html', context)

@staff_member_required
def admin_process_withdrawal(request, withdrawal_id):
    """Admin process withdrawal request"""
    print(f"DEBUG: admin_process_withdrawal view called for withdrawal_id: {withdrawal_id}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request user: {request.user}")
    
    withdrawal_request = get_object_or_404(WithdrawalRequest, id=withdrawal_id)
    transaction = withdrawal_request.transaction
    
    print(f"DEBUG: Found withdrawal_request: {withdrawal_request}")
    print(f"DEBUG: Found transaction: {transaction}")
    print(f"DEBUG: Transaction status: {transaction.status}")

    if request.method == 'POST':
        print(f"DEBUG: Processing withdrawal {withdrawal_id}")
        print(f"DEBUG: POST data: {request.POST}")
        print(f"DEBUG: Current transaction status: {transaction.status}")
        
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        transaction_hash = request.POST.get('transaction_hash', '')

        print(f"DEBUG: Action: {action}")
        print(f"DEBUG: Admin notes: {admin_notes}")
        print(f"DEBUG: Transaction hash: {transaction_hash}")

        if action == 'approve':
            print(f"DEBUG: Approving withdrawal {withdrawal_id}")
            # Check if user has sufficient balance first
            try:
                user_wallet = UserWallet.objects.get(
                    user=transaction.user,
                    crypto_type=transaction.crypto_type
                )
                print(f"DEBUG: User wallet balance: {user_wallet.balance}")
                print(f"DEBUG: Withdrawal amount: {transaction.amount}")

                if user_wallet.balance < transaction.amount:
                    print(f"DEBUG: Insufficient balance!")
                    messages.error(request, f'Insufficient balance. User has {user_wallet.balance} {transaction.crypto_type}, but trying to withdraw {transaction.amount}')
                    return redirect('admin_transactions')
            except UserWallet.DoesNotExist:
                print(f"DEBUG: User wallet not found!")
                messages.error(request, 'User wallet not found.')
                return redirect('admin_transactions')

            # Update transaction status to completed (one-step approval)
            print(f"DEBUG: Updating transaction status to completed")
            transaction.status = 'completed'
            transaction.approved_by = request.user
            transaction.approved_at = timezone.now()
            transaction.completed_at = timezone.now()
            transaction.admin_notes = admin_notes
            transaction.save()
            print(f"DEBUG: Transaction saved with status: {transaction.status}")

            # Update withdrawal request
            print(f"DEBUG: Updating withdrawal request")
            withdrawal_request.processed_by = request.user
            withdrawal_request.processed_at = timezone.now()
            withdrawal_request.sent_at = timezone.now()
            withdrawal_request.processing_notes = admin_notes
            withdrawal_request.save()

            # Deduct from user wallet
            old_balance = user_wallet.balance
            user_wallet.balance -= transaction.amount
            user_wallet.save()
            print(f"DEBUG: Updated wallet balance from {old_balance} to {user_wallet.balance}")

            # Create notification
            TransactionNotification.objects.create(
                user=transaction.user,
                transaction=transaction,
                title='Withdrawal Approved',
                message=f'Your withdrawal of {transaction.amount} {transaction.crypto_type} has been approved and processed.',
                notification_type='withdrawal_completed'
            )

            messages.success(request, f'Withdrawal approved! Deducted {transaction.amount} {transaction.crypto_type} from user wallet. New balance: {user_wallet.balance}')
            print(f"DEBUG: Redirecting to admin_transactions")
            return redirect('admin_transactions')

        elif action == 'complete':
            print(f"DEBUG: Completing withdrawal {withdrawal_id}")
            # Mark as completed with transaction hash
            transaction.status = 'completed'
            transaction.transaction_hash = transaction_hash
            transaction.completed_at = timezone.now()
            transaction.admin_notes = admin_notes
            transaction.save()

            withdrawal_request.sent_transaction_hash = transaction_hash
            withdrawal_request.sent_at = timezone.now()
            withdrawal_request.processing_notes = admin_notes
            withdrawal_request.save()

            # Create notification
            TransactionNotification.objects.create(
                user=transaction.user,
                transaction=transaction,
                title='Withdrawal Completed',
                message=f'Your withdrawal of {transaction.amount} {transaction.crypto_type} has been sent.',
                notification_type='withdrawal_completed'
            )

            messages.success(request, 'Withdrawal marked as completed.')
            print(f"DEBUG: Redirecting to admin_transactions")
            return redirect('admin_transactions')

        elif action == 'reject':
            print(f"DEBUG: Rejecting withdrawal {withdrawal_id}")
            transaction.status = 'rejected'
            transaction.approved_by = request.user
            transaction.approved_at = timezone.now()
            transaction.rejection_reason = admin_notes
            transaction.admin_notes = admin_notes
            transaction.save()

            withdrawal_request.processing_notes = admin_notes
            withdrawal_request.save()

            messages.warning(request, 'Withdrawal request rejected.')
            print(f"DEBUG: Redirecting to admin_transactions")
            return redirect('admin_transactions')
        else:
            print(f"DEBUG: Invalid action: {action}")
            print(f"DEBUG: Action type: {type(action)}")
            print(f"DEBUG: All POST keys: {list(request.POST.keys())}")
            messages.error(request, f'Invalid action: {action}')
            return redirect('admin_transactions')

    print(f"DEBUG: Rendering admin_process_withdrawal template")
    context = {
        'withdrawal_request': withdrawal_request,
        'transaction': transaction,
    }

    return render(request, 'transactions/admin_process_withdrawal.html', context)
