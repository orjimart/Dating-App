# recover_password.py
from django.shortcuts import render, redirect
from django.contrib import messages

def recover_password(request):
    reset_code = request.session.get('reset_code')
    reset_email = request.session.get('reset_email')

    # Ensure session data exists
    if not reset_code or not reset_email:
        messages.error(request, 'Password reset session has expired. Please try again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        entered_code = request.POST.get('username')

        if entered_code and int(entered_code) == reset_code:
            # Code matches, proceed to set a new password
            return redirect('new_password')
        else:
            messages.error(request, 'Invalid recovery code.')

    return render(request, 'recover_password.html')
