import os

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import UserInfoForm, UserLoginForm, UserEmailForm, UserAvatarForm
from django.contrib.auth.forms import PasswordChangeForm
from main.models import MyFavorites, TrainingProgram
from training_app.models import Achievements


@login_required
def profile(request):
    context = {}
    if request.user.training.all().exists():
        context['training'] = request.user.training.select_related('train_program').first()
    return render(request, 'user_profile/user_profile.html', context)


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


class FavoriteList(ListView):
    model = MyFavorites
    template_name = 'user_profile/favorite_exercises.html'
    context_object_name = 'exercise_list'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        if self.request.GET.get('category'):
            return self.request.user.favorite.filter(category=self.request.GET.get('category'))\
                .select_related('exercise').all()
        return self.request.user.favorite.select_related('exercise').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteList, self).get_context_data(**kwargs)
        context['categories'] = self.request.user.favorite.values_list('category', flat=True).distinct()
        if self.request.GET.get('category'):
            context['category_section'] = self.request.GET.get('category')
        return context


class AchievementsList(ListView):
    model = Achievements
    context_object_name = 'achievements'
    template_name = 'user_profile/achievements_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return self.request.user.achievements.select_related('exercise').prefetch_related('exercise__category').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AchievementsList, self).get_context_data(**kwargs)
        context['categories'] = self.object_list.values_list('exercise__category__title', flat=True).distinct()
        return context


@login_required
def delete_from_favorite(request, pk):
    favorite = MyFavorites.objects.get(pk=pk)
    favorite.delete()
    return redirect('favorite_exercises')
