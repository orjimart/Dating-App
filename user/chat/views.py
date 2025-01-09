from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ChatRoom, Message
from django.http import JsonResponse

@login_required
def chat_list(request):
    # Get all chat rooms for the current user
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chat/chat_list.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    # Ensure user is a participant
    if request.user not in room.participants.all():
        return HttpResponseForbidden("You don't have access to this chat room")
    
    messages = room.messages.all()
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages
    })

@login_required
def create_chat_room(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)
    
    # Check if they are friends
    if friend not in request.user.friends.all():
        return JsonResponse({'error': 'You must be friends to start a chat'}, status=403)
    
    # Check if a chat room already exists
    chat_room = ChatRoom.objects.filter(participants=request.user)\
        .filter(participants=friend).first()
    
    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(request.user, friend)
    
    return JsonResponse({'room_id': chat_room.id})
