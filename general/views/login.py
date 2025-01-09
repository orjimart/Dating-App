from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login with Username: {username}")

        User = get_user_model()  # Fetch the custom user model
        try:
            # Use the custom user model to fetch the user
            user = User.objects.filter(username=username).first()
            
            # Debugging
            if user:
                print(f"User found: {user}")
                print(f"Stored password hash: {user.password}")
            else:
                print(f"No user found with username: {username}")
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request, 'login.html')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Password is correct")
                auth_login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('self_profile')
            else:
                print("Password is incorrect")
                messages.error(request, 'Invalid username or password. Please try again.')
        except Exception as e:
            print(f"An error occurred: {e}")
            messages.error(request, 'An error occurred. Please try again later.')

    return render(request, 'login.html')
