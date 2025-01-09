from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('community/', views.community, name='community'),
    path('membership/', views.membership, name='membership'),
    path('blogs/', views.blogs, name='blogs'),
    path('shop/', views.shop, name='shop'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recover_password/', views.recover_password, name='recover_password'),
    path('new_password/', views.new_password, name='new_password'),




]
