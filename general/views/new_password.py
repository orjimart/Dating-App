# new_password.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

def new_password(request):
    reset_email = request.session.get('reset_email')

    # Ensure session data exists
    if not reset_email:
        messages.error(request, 'Password reset session has expired. Please try again.')
        return redirect('forgot_password')

    User = get_user_model()

    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('password_confirm')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'new_password.html')

        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'new_password.html')

        try:
            user = User.objects.get(email=reset_email)
            user.password = make_password(password1)
            user.save()

            # Clear session data after password reset
            del request.session['reset_code']
            del request.session['reset_email']

            messages.success(request, 'Password reset successfully! Please log in with your new password.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'new_password.html')
