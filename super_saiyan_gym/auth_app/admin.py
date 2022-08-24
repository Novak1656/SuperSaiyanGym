from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'train_program', 'email', 'first_name', 'last_name', 'last_login', 'is_active',)
    list_display_links = ('id', 'username',)
    search_fields = ('username',)
    list_filter = ('sex', 'date_of_birth',)
