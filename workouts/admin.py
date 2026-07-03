"""
workouts/admin.py
"""
from django.contrib import admin
from .models import WorkoutLog


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display  = ['user', 'workout_type', 'duration', 'intensity', 'steps', 'calories_predicted', 'date']
    list_filter   = ['workout_type', 'date']
    search_fields = ['user__username']
