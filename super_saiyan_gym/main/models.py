from django.db import models
from django.urls import reverse


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
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['category']

    def __str__(self):
        return f"{self.category}: {self.title}"


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
