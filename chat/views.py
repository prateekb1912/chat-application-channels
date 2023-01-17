from django.shortcuts import render

# Create your views here.

def lobby(request):
    return render(request, 'lobby.html')

def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})