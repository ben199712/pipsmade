from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .email_notifications import send_login_notification, send_signup_notification

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'accounts/login.html')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Send admin notification email using the simple email system
            try:
                send_login_notification(user)
                print(f"Login notification sent successfully for user {user.username}")
            except Exception as e:
                # Log error but don't fail login
                print(f"Failed to send login notification: {e}")

            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

@csrf_protect
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Basic validation
        if not all([email, password, first_name, last_name]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/signup.html')

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'accounts/signup.html')

        # Create user
        try:
            username = email  # Use email as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Send admin notification email using the simple email system
            try:
                send_signup_notification(user)
                print(f"Signup notification sent successfully for user {user.username}")
            except Exception as e:
                # Log error but don't fail registration
                print(f"Failed to send signup notification: {e}")

            # Auto login after registration
            login(request, user)
            messages.success(request, f'Welcome to pipsmade, {user.get_full_name()}!')
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
