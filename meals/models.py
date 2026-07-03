"""
meals/models.py
"""
from django.db import models
from django.contrib.auth.models import User


class MealLog(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch',     'Lunch'),
        ('dinner',    'Dinner'),
        ('snack',     'Snack'),
    ]

    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals')
    meal_name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, default='lunch')
    calories  = models.FloatField()
    protein   = models.FloatField(default=0, help_text="Grams of protein")
    carbs     = models.FloatField(default=0, help_text="Grams of carbohydrates")
    fats      = models.FloatField(default=0, help_text="Grams of fat")
    date      = models.DateField(auto_now_add=True)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.meal_name} ({self.date})"
