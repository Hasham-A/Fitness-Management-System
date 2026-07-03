"""
meals/admin.py
"""
from django.contrib import admin
from .models import MealLog


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display  = ['user', 'meal_name', 'meal_type', 'calories', 'protein', 'carbs', 'fats', 'date']
    list_filter   = ['meal_type', 'date']
    search_fields = ['user__username', 'meal_name']
