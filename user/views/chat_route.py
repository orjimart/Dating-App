from django.shortcuts import render


def chat_route(request):
 
    return render(request, 'chat_route.html')
