"""
accounts/models.py
Stores the extended user profile with fitness-specific data.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]

    GOAL_CHOICES = [
        ('weight_loss',    'Weight Loss'),
        ('muscle_gain',    'Muscle Gain'),
        ('maintenance',    'Maintenance'),
        ('endurance',      'Endurance'),
    ]

    ACTIVITY_CHOICES = [
    ('sedentary',    'Sedentary (desk job, no exercise)'),
    ('light',        'Light (1–3 days/week)'),
    ('moderate',     'Moderate (3–5 days/week)'),
    ('active',       'Active (6–7 days/week)'),
    ('very_active',  'Very Active (athlete / physical job)'),
]

    EXPERIENCE_CHOICES = [
    ('beginner',     'Beginner (0–1 year training)'),
    ('intermediate', 'Intermediate (1–3 years training)'),
]

    # One profile per user — delete profile when user is deleted
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age         = models.PositiveIntegerField(null=True, blank=True)
    height      = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight      = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    gender      = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    fitness_goal= models.CharField(max_length=20, choices=GOAL_CHOICES, default='maintenance')
    activity_level   = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    waist       = models.FloatField(null=True, blank=False, help_text="Waist circumference in cm")
    chest       = models.FloatField(null=True, blank=False, help_text="Chest circumference in cm")
    hip         = models.FloatField(null=True, blank=False, help_text="Hip circumference in cm")
    thigh       = models.FloatField(null=True, blank=False, help_text="Thigh circumference in cm")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def bmi(self):
        """Calculate Body Mass Index from height and weight."""
        if self.height and self.weight and self.height > 0:
            height_m = self.height / 100  # convert cm to metres
            return round(self.weight / (height_m ** 2), 1)
        return None

    def bmi_category(self):
        """Return a human-friendly BMI category label."""
        bmi = self.bmi()
        if bmi is None:
            return "N/A"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        return "Obese"

    def __str__(self):
        return f"{self.user.username}'s Profile"
