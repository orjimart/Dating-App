from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from ..models import FriendRequest


@login_required
def friend_request(request):
    # Get all friend requests sent to the logged-in user
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    # Calculate the age of the user (the logged-in user)
    if request.user.birthday:
        today = datetime.today()
        age = today.year - request.user.birthday.year - ((today.month, today.day) < (request.user.birthday.month, request.user.birthday.day))
    else:
        age = None

    context = {
        'friend_requests': friend_requests,
        'age': age  # Pass age to template
    }
    
    return render(request, 'friend_request.html', context)
