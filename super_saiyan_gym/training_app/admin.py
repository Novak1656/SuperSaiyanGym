from django.contrib import admin
from .models import Schedules, Training, Achievements, TrainingProcess, ExerciseLvlUp


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'train_program', 'mailing',)
    list_display_links = ('id', 'user',)
    list_filter = ('train_program', 'mailing',)


@admin.register(Schedules)
class SchedulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'training', 'day',)
    list_display_links = ('id',)
    list_filter = ('training', 'day',)


@admin.register(Achievements)
class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exercise', 'achieve_param', 'created_at', 'updated_at',)
    list_display_links = ('id', 'user',)
    list_filter = ('user', 'exercise', 'achieve_param', 'created_at', 'updated_at',)
    search_fields = ('user', 'exercise',)


@admin.register(TrainingProcess)
class TrainingProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'started_at',)
    list_display_links = ('id', 'user',)
    list_filter = ('started_at', 'user',)


@admin.register(ExerciseLvlUp)
class ExerciseLvlUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'training_process', 'exercise_id', 'old_achieve_param', 'new_achieve_param',)
    list_display_links = ('id', 'training_process',)
