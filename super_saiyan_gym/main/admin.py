from django.contrib import admin
from .models import TrainingProgram, Exercises, ExercisesCategory, MyFavorites


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
    list_display = ('id', 'title', 'category', 'description', 'like', 'created_at', 'updated_at',)
    list_display_links = ('id', 'title',)
    list_filter = ('title', 'created_at', 'category', 'like',)
    search_fields = ('title',)
    save_as = True


@admin.register(ExercisesCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(MyFavorites)
class MyFavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'exercise', 'category',)
    list_display_links = ('id', 'user',)
    list_filter = ('user', 'category',)
    search_fields = ('user', 'exercise',)
