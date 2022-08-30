from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('training_programs/<str:slug>/', TrainProgramDetail.as_view(), name='program_detail'),
    path('training_programs/', TrainProgramList.as_view(), name='program_list'),

    path('add_in_favorite/<int:pk>/', add_in_favorites, name='add_in_favorite'),

    path('exercises_list/', ExercisesList.as_view(), name='exercises_list'),
    path('exercises_list/search/', ExercisesSearchList.as_view(), name='exercises_search_list'),

    path('exercises_list/category/<str:cat_title>', ExercisesByCategoryList.as_view(), name='exercises_category_list'),
    path('exercises_list/category/<str:cat_title>/search/', ExercisesByCategorySearchList.as_view(),
         name='exercises_category_search_list'),

    path('exercises_detail/<int:pk>', ExercisesDetail.as_view(), name='exercises_detail'),

]
