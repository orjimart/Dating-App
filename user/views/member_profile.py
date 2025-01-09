from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from general.models import CustomUser
from ..models import FriendRequest

@login_required
def member_profile(request, user_id):
    # Get the user whose profile is being viewed
    profile_user = get_object_or_404(CustomUser, id=user_id)   

    # Calculate age based on birthday
    if profile_user.birthday:
        today = datetime.today()
        age = today.year - profile_user.birthday.year - ((today.month, today.day) < (profile_user.birthday.month, profile_user.birthday.day))
    else:
        age = None

    # Get the current user's sent friend requests
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    sent_requests_ids = sent_requests.values_list('to_user_id', flat=True)

    # Check if the two users are already friends
    are_friends = request.user.friends.filter(id=profile_user.id).exists()

    # Cover photo check
    cover_photo = profile_user.cover_photo.url if profile_user.cover_photo else None

    context = {
        'profile_user': profile_user,
        'age': age,
        'cover_photo': cover_photo,
        'sent_requests_ids': sent_requests_ids,  # Pass sent requests to template
        'are_friends': are_friends,  # Pass friend status to template
    }

    return render(request, 'member_profile.html', context)
