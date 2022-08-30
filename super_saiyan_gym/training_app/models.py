from django.db import models
from auth_app.models import User
from main.models import ExercisesCategory, TrainingProgram, Exercises


class Training(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE, related_name='training')
    train_program = models.ForeignKey(verbose_name='Тренировочная программа', to=TrainingProgram,
                                      on_delete=models.PROTECT, related_name='training')
    mailing = models.BooleanField('Рассылка уведомлений', default=0)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['pk']

    def __str__(self):
        return f"{self.user}"


class Schedules(models.Model):
    DAYS = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье')
    ]
    training = models.ForeignKey(verbose_name='Тренировка', to=Training, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField('День недели', choices=DAYS, max_length=255)
    exercises = models.ManyToManyField(verbose_name='Упражнения', to=ExercisesCategory, related_name='schedules')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-day']

    def __str__(self):
        return f"Schedule {self.pk}"


class Achievements(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE,
                             related_name='achievements')
    exercise = models.ForeignKey(verbose_name='Упражнение', to=Exercises, on_delete=models.CASCADE,
                                 related_name='achievements')
    achieve_param = models.DecimalField('Показатели', max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-user']

    def __str__(self):
        return f"#{self.pk}: {self.user}"
