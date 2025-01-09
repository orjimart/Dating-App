# forgot_password.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import random

# Function to generate a 6-digit code
def generate_reset_code():
    return random.randint(100000, 999999)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return render(request, 'forgot_password.html')

        # Generate reset code and store in session
        reset_code = generate_reset_code()
        request.session['reset_code'] = reset_code
        request.session['reset_email'] = email

        # Send email with the reset code
        send_mail(
            'Password Reset Code',
            f'Your password reset code is {reset_code}.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        messages.success(request, 'A reset code has been sent to your email.')
        return redirect('recover_password')

    return render(request, 'forgot_password.html')
