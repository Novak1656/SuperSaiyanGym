from django.urls import path
from .views import *

urlpatterns =[
    path('', profile, name='profile'),
    path('config/', profile_config, name='profile_config'),
]
