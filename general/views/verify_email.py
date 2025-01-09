# views/verify_email.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib import messages
from ..models import CustomUser  # Use the correct import for your custom user model

def verify_email(request):
    # Check if the user_id and verification_code are in session
    user_id = request.session.get('user_id')
    verification_code = request.session.get('verification_code')

    # Debugging session data
    print(f"User ID in session: {user_id}")
    print(f"Verification code in session: {verification_code}")

    # If session data is missing, redirect to register with a message
    if not user_id or not verification_code:
        messages.error(request, 'Verification session expired. Please register again.')
        return redirect('register')

    # Handle the POST request for verification
    if request.method == 'POST':
        entered_code = request.POST.get('code')

        # Check if the entered code matches the session code
        if entered_code and int(entered_code) == verification_code:
            # Correct the model being queried here
            user = get_object_or_404(CustomUser, id=user_id)
            
            # Check if the user is already active/verified to prevent repeated activation
            if user.is_active:
                messages.info(request, 'Your email is already verified.')
                return redirect('self_profile')

            # Activate the user and update email verification status
            user.is_active = True
            user.email_verified = True  # Assuming you have this field in CustomUser
            user.save()

            # Clear session variables to prevent reuse
            del request.session['verification_code']
            del request.session['user_id']

            # Log the user in
            auth_login(request, user)
            messages.success(request, 'Email verified successfully! Welcome to your profile.')
            return redirect('self_profile')
        else:
            messages.error(request, 'Invalid verification code.')

    # Render the email verification page with a form to input the code
    return render(request, 'verify_email.html')
