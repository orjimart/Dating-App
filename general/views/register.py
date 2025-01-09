from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login as auth_login
from ..forms import RegistrationForm
from ..models import CustomUser
import random

# Function to generate a 6-digit verification code
def generate_verification_code():
    return random.randint(100000, 999999)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'register.html', {'form': form})

            # Check password length
            if len(password1) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return render(request, 'register.html', {'form': form})

            # Save user data but deactivate the account
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email verification

            # Hash the password before saving the user
            user.set_password(password1)
            user.save()

            # Generate and store verification code in session
            verification_code = generate_verification_code()
            request.session['verification_code'] = verification_code
            request.session['user_id'] = user.id

            # Send verification code via email
            send_mail(
                'Email Verification Code',
                f'Your verification code is {verification_code}.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            # Automatically log the user in after registration
            auth_login(request, user)
            messages.success(request, 'Registration successful! Please verify your email.')

            # Redirect to verification page
            return redirect('verify_email')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
