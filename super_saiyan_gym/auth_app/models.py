import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import TrainingProgram


def get_avatar_path(instance, filename):
    return f"img/user_avatars/{instance.username}/{filename}"


class User(AbstractUser):
    SEX = [
        ('Man', 'Мужской'),
        ('Women', 'Женский')
    ]

    date_of_birth = models.DateField('Дата рождения', null=True)
    sex = models.CharField('Пол', choices=SEX, max_length=10, default='Man')
    weight = models.DecimalField('Вес', max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField('Рост', max_digits=5, decimal_places=2, null=True)
    avatar = models.ImageField('Аватар', upload_to=get_avatar_path, blank=True, null=True)
    train_program = models.ForeignKey(verbose_name='Тренировочная программа', to=TrainingProgram,
                                      on_delete=models.PROTECT, related_name='user', null=True)

    class Meta:
        ordering = ['date_joined']
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
