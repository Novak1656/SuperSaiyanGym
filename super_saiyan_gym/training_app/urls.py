from django.urls import path
from .views import *

urlpatterns = [
    path('', dojo, name='dojo'),
    path('in_training/', training_process, name='in_training'),
    path('training_conf/', training_conf, name='training_conf'),
    path('update_schedule/<int:pk>/', update_schedule, name='update_schedule'),

    path('start_mailing/', start_mailing, name='start_mailing'),
    path('start_training/', create_training, name='start_training'),
    path('end_training/', delete_training, name='end_training'),
]
