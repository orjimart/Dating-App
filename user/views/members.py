from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from general.models import CustomUser
from ..models import FriendRequest

@login_required
def members(request):
    # Exclude the current user from the list of users
    users = CustomUser.objects.exclude(id=request.user.id)
    
    # Paginate users (10 per page)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the current user's sent friend requests
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    sent_requests_ids = sent_requests.values_list('to_user_id', flat=True)

    # Create a list of user IDs who are already friends with the current user
    friends_ids = request.user.friends.values_list('id', flat=True)

    context = {
        'page_obj': page_obj,
        'sent_requests_ids': sent_requests_ids,
        'friends_ids': friends_ids,  # Pass the list of friend IDs to the template
    }
    return render(request, 'members.html', context)


@login_required
def send_friend_request(request, user_id):
    # Send a friend request to a specific user
    to_user = get_object_or_404(CustomUser, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    
    return redirect('members')

@login_required
def cancel_friend_request(request, user_id):
    # Cancel a friend request to a specific user
    to_user = get_object_or_404(CustomUser, id=user_id)
    friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).first()
    
    if friend_request:
        friend_request.delete()  # Delete the friend request
    
    return redirect('members')


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if friend_request.to_user == request.user:
        friend_request.from_user.friends.add(request.user)
        request.user.friends.add(friend_request.from_user)
        friend_request.delete()
        return redirect('chat_route')  
    return redirect('self_profile')  



@login_required
def delete_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if friend_request.to_user == request.user:
        friend_request.delete()
        return redirect('friend_request')  
    return redirect('self_profile')