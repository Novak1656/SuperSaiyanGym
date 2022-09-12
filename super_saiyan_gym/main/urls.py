from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('training_programs/program/<str:slug>/', TrainProgramDetail.as_view(), name='program_detail'),
    path('training_programs/', TrainProgramList.as_view(), name='program_list'),
    path('training_programs/search/', TrainProgramSearchList.as_view(), name='program_list_search'),
    path('training_programs/category/<str:category>', TrainProgramListByCategory.as_view(), name='program_list_cat'),
    path('training_programs/category/<str:category>/search/',
         TrainProgramSearchListByCategory.as_view(), name='program_list_cat_search'),

    path('create_custom_program/', UserCreateTrainProgramView.as_view(), name='create_custom_program'),

    path('add_in_favorite/<int:pk>/', add_in_favorites, name='add_in_favorite'),

    path('exercises_list/', ExercisesList.as_view(), name='exercises_list'),
    path('exercises_list/search/', ExercisesSearchList.as_view(), name='exercises_search_list'),

    path('exercises_list/category/<str:cat_title>', ExercisesByCategoryList.as_view(), name='exercises_category_list'),
    path('exercises_list/category/<str:cat_title>/search/', ExercisesByCategorySearchList.as_view(),
         name='exercises_category_search_list'),

    path('exercises_detail/<int:pk>', ExercisesDetail.as_view(), name='exercises_detail'),

]
