"""
accounts/admin.py — Register models with Django admin panel.
"""
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'age', 'weight', 'height', 'gender', 'fitness_goal', 'bmi']
    list_filter   = ['gender', 'fitness_goal']
    search_fields = ['user__username', 'user__email']
