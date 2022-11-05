from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')
    

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                print(request.POST)
                username = request.POST['username']
                password = request.POST['password1']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('tasks')
            else:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'submit_message': 'Passwords do not mach'
                })
        except IntegrityError:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'submit_message': 'User already exist'
                })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'User or password incorrect'
                })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')
