from django.contrib import admin
from .models import TrainingProgram, Exercises, ExercisesCategory


@admin.register(TrainingProgram)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'created_at', 'updated_at',)
    list_display_links = ('id', 'title', 'slug',)
    list_filter = ('title', 'created_at',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_as = True


@admin.register(Exercises)
class ExercisesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at',)
    list_display_links = ('id', 'title',)
    list_filter = ('title', 'created_at', 'category',)
    search_fields = ('title',)
    save_as = True


@admin.register(ExercisesCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    list_filter = ('title',)
    search_fields = ('title',)
