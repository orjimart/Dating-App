from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from general.models import CustomUser

@login_required
def unfriend(request, user_id):
    # Get the user to unfriend
    to_unfriend = get_object_or_404(CustomUser, id=user_id)

    # Check if the current user and the selected user are friends
    if request.user.friends.filter(id=to_unfriend.id).exists():
        # Remove the friendship
        request.user.friends.remove(to_unfriend)
        to_unfriend.friends.remove(request.user)

        return redirect('self_profile')  # Redirect to the current user's profile or another appropriate page
    else:
        # If they are not friends, handle accordingly
        return redirect('self_profile')  # Optionally redirect to another page with a message
