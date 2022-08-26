from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django_unique_slugify import unique_slugify, slugify
from unidecode import unidecode


class ExercisesCategory(models.Model):
    title = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Exercises(models.Model):
    title = models.CharField('Название', max_length=255)
    category = models.ForeignKey(verbose_name='Категория', to=ExercisesCategory,
                                 on_delete=models.CASCADE, related_name='exercises')
    description = models.TextField('Описание', blank=True, null=True)
    like = models.IntegerField('Понравилось', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['category']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('exercises_detail', kwargs={'pk': self.pk})


class TrainingProgram(models.Model):
    slug = models.SlugField('Слаг', max_length=255)
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    days_in_week = models.IntegerField('Занятий в неделю')
    training_count = models.IntegerField('Количество занятий', default=8)
    retry_exercises = models.IntegerField('Кол-во повторений упражнений')
    exercises = models.ManyToManyField(verbose_name='Упражнения', to=Exercises, related_name='train_program')
    prise = models.DecimalField('Цена', max_digits=5, decimal_places=2)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Тренировочная программа'
        verbose_name_plural = 'Программы тренировок'
        ordering = ['prise']

    def __str__(self):
        return f"Program: {self.title}"

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, slugify(unidecode(self.title)))
        super(TrainingProgram, self).save(*args, **kwargs)


class MyFavorites(models.Model):
    user = models.ForeignKey('auth_app.User', verbose_name='Пользователь',
                             on_delete=models.CASCADE, related_name='favorite')
    exercise = models.ForeignKey(Exercises, verbose_name='Упражнение',
                                 on_delete=models.CASCADE, related_name='favorite')
    category = models.CharField('Категория', max_length=255, default='Бицепс')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
