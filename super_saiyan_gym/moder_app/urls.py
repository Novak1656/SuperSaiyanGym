from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='moder'),

    path('moder_create/program/', ModerCreateProgramView.as_view(), name='moder_create_program'),
    path('moder_create/category/', ModerCreateCategoryView.as_view(), name='moder_create_category'),
    path('moder_create/exercise/', ModerCreateExerciseView.as_view(), name='moder_create_exercise'),
    path('moder_create/program_category/', ModerCreateProgramCategoryView.as_view(), name='moder_create_pro_cat'),

    path('moder_update/program/<int:pk>/', ModerUpdateProgram.as_view(), name='moder_update_program'),
    path('moder_update/category/<int:pk>/', ModerUpdateCategory.as_view(), name='moder_update_category'),
    path('moder_update/exercise/<int:pk>/', ModerUpdateExercise.as_view(), name='moder_update_exercise'),
    path('moder_update/program_category/<int:pk>', ModerUpdateProgramCategory.as_view(), name='moder_update_pro_cat'),

    path('moder_delete/program/<int:pk>/', ModerDeleteProgram.as_view(), name='moder_delete_program'),
    path('moder_delete/category/<int:pk>/', ModerDeleteCategory.as_view(), name='moder_delete_category'),
    path('moder_delete/exercise/<int:pk>/', ModerDeleteExercise.as_view(), name='moder_delete_exercise'),
    path('moder_delete/program_category/<int:pk>', ModerDeleteProgramCategory.as_view(), name='moder_delete_pro_cat'),

    path('suggestions/<str:slug>/', get_suggestion, name='get_suggestion'),
    path('suggestions/delete/<str:slug>/', delete_suggestion, name='delete_suggestion')
]

