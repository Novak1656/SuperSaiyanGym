from django.urls import path
from .views import *

urlpatterns =[
    path('', profile, name='profile'),
    path('config/', profile_config, name='profile_config'),
    path('favorite_exercises/', FavoriteList.as_view(), name='favorite_exercises'),
    path('my_achievements/', AchievementsList.as_view(), name='my_achievements'),
    path('delete_from_favorite/<int:pk>', delete_from_favorite, name='delete_from_favorite'),
]
