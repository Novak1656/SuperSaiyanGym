from django import forms
from auth_app.models import User
from django.core.exceptions import ValidationError


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'sex', 'weight', 'height',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию...'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=User.SEX, attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш вес...'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш рост...'}),
        }

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight < 1:
            raise ValidationError('Показатель веса не может быть отрицательным')
        return weight

    def clean_height(self):
        height = self.cleaned_data['height']
        if height < 1:
            raise ValidationError('Показатель роста не может быть отрицательным')
        return height


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый логин...'})
        }


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('Данный адрес электронной почты уже занят')
        return self.cleaned_data


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }
