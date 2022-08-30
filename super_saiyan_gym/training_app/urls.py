from django.urls import path
from .views import *

urlpatterns = [
    path('', dojo, name='dojo'),
    path('training_conf/', training_conf, name='training_conf'),
    path('start_mailing/', start_mailing, name='start_mailing'),
    path('start_training/', create_training, name='start_training'),
    path('end_training/', delete_training, name='end_training'),
]
