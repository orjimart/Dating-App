from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout
from general.models import CustomUser
from ..models import FriendRequest
from django.http import JsonResponse
from random import sample
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout



@login_required
def self_profile(request):
    user = request.user

    # Calculate the age of the user
    if user.birthday:
        today = datetime.today()
        age = today.year - user.birthday.year - ((today.month, today.day) < (user.birthday.month, user.birthday.day))
    else:
        age = None  

    # Get user's cover photo if it exists
    cover_photo = user.cover_photo.url if user.cover_photo else None

    # Get the user's friends
    friends = user.friends.all()
    num_friends = friends.count()  # Count of friends

    # Get the number of friend requests the user has received
    friend_requests = FriendRequest.objects.filter(to_user=user)
    num_friend_requests = friend_requests.count()  # Count of friend requests

    # For initial page load, show random users who are not friends
    all_users = CustomUser.objects.exclude(id=user.id).exclude(id__in=friends.values_list('id', flat=True))
    friends_to_display = sample(list(all_users), min(3, len(all_users)))

    context = {
        'user': user,
        'age': age,
        'cover_photo': cover_photo,
        'friends_to_display': friends_to_display,
        'friend_type': "random_users",
        'num_friends': num_friends,  # Add number of friends to context
        'num_friend_requests': num_friend_requests,  # Add number of friend requests to context
    }

    return render(request, 'self_profile.html', context)


@login_required
def get_friends(request):
    user = request.user
    friends = user.friends.all()
    friends_data = [
        {
            'id': friend.id,
            'username': friend.username,
            'cover_photo': friend.cover_photo.url if friend.cover_photo else None,
            'date_joined': friend.date_joined.strftime('%B %Y')
        }
        for friend in friends
    ]
    return JsonResponse({'friends': friends_data})





def user_logout(request):
    logout(request)
    return redirect('home')
