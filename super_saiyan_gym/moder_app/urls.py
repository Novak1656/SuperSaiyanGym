from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='moder'),
    path('moder_create/', ModerCreateView.as_view(), name='moder_create')
]

