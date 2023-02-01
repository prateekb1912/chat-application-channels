from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.

def register_user(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful." )
                
                return redirect('index')
            messages.error(request, "Unsuccessful registration. Invalid information.")

        form = UserCreationForm()
        context = {'register_form': form}

        return render(request, 'registration/register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    
    form = AuthenticationForm()
    context = {'login_form': form}

    return render(request, 'registration/login.html', context)

def index(request):
    return render(request, 'lobby.html')

def room(request, room_name):
    return render(request, 'room.html', {'room_name': room_name})