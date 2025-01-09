from django.urls import path
from . import views

urlpatterns = [
    path('', views.self_profile, name='self_profile'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('self_profile/', views.self_profile, name='self_profile'),
    path('get_friends/', views.get_friends, name='get_friends'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('members/', views.members, name='members'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('members/profile/<int:user_id>/', views.member_profile, name='member_profile'), 
    path('cancel_friend_request/<int:user_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/delete/<int:request_id>/', views.delete_friend_request, name='delete_friend_request'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
    path('chat_route/', views.chat_route, name='chat_route'),



]
