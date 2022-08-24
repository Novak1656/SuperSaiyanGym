from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('training_programs/<str:slug>/', TrainProgramDetail.as_view(), name='program_detail'),
    path('training_programs/', TrainProgramList.as_view(), name='program_list'),
    path('start_training/', start_training, name='start_training'),
    path('end_training/', end_training, name='end_training'),
]
