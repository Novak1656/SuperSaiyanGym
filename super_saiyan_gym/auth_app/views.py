import os

from django.conf import settings
from django.contrib.auth import logout, login
from django.core.files import File
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm


def register(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            with open(os.path.join(settings.BASE_DIR, 'auth_app/static/auth_app/img/default_avatar.jpg'), 'rb') as f:
                avatar_file = File(f)
                user.avatar.safe('default_avatar.jpg', avatar_file, True)
            user.save()
            login(request, user)
            return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = form.cleaned_data['remember_me']
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
            login(request, user)
            return redirect('main')
    else:
        form = LoginForm()
    return render(request, 'auth_app/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
