from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('log/',          views.log_workout,     name='log'),
    path('log/<int:pk>/', views.update_workout,  name='update'),
    path('delete/<int:pk>/', views.delete_workout, name='delete'),
    path('history/',      views.workout_history, name='history'),
]
