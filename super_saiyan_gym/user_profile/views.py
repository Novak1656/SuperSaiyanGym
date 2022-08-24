import os

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserInfoForm, UserLoginForm, UserEmailForm, UserAvatarForm
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def profile(request):
    return render(request, 'user_profile/user_profile.html')


@login_required
def profile_config(request):
    user = request.user

    def get_form(conf_value):
        forms = {'user_info': UserInfoForm(instance=user), 'login': UserLoginForm(instance=user),
                 'email': UserEmailForm(instance=user), 'password': PasswordChangeForm(user=user),
                 'avatar': UserAvatarForm()}
        return forms.get(conf_value)

    if request.method == 'POST':
        if request.GET.get('conf') == 'user_info':
            form = UserInfoForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        elif request.GET.get('conf') == 'login':
            form = UserLoginForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        elif request.GET.get('conf') == 'email':
            form = UserEmailForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        elif request.GET.get('conf') == 'avatar':
            old_avatar = request.user.avatar.path
            form = UserAvatarForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                os.remove(old_avatar)
                form.save()
                return redirect('profile')
        else:
            form = PasswordChangeForm(data=request.POST, user=user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)
                return redirect('profile')
    else:
        form = get_form(request.GET.get('conf'))
    context = {'form': form, 'cur_conf': request.GET.get('conf'),
               'conf_data': [('user_info', 'Общие сведенья'), ('login', 'Логин'), ('email', 'Электронная почта'),
                             ('password', 'Пароль'), ('avatar', 'Аватар')]}
    return render(request, 'user_profile/profile_config.html', context)
