from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('log/',          views.log_meal,     name='log'),
    path('log/<int:pk>/', views.update_meal,  name='update'),
    path('delete/<int:pk>/', views.delete_meal, name='delete'),
    path('history/',      views.meal_history, name='history'),
]
