"""
workouts/models.py
Stores each workout session and the ML-predicted calorie burn.
"""
from django.db import models
from django.contrib.auth.models import User


class WorkoutLog(models.Model):
    WORKOUT_TYPES = [
        ('running',   'Running'),
        ('cycling',   'Cycling'),
        ('swimming',  'Swimming'),
        ('walking',   'Walking'),
        ('weightlifting', 'Weight Lifting'),
        ('yoga',      'Yoga'),
        ('hiit',      'HIIT'),
        ('other',     'Other'),
    ]

    INTENSITY_CHOICES = [(i, str(i)) for i in range(1, 11)]  # 1 (easy) to 10 (max)

    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    workout_type      = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    duration          = models.PositiveIntegerField(help_text="Duration in minutes")
    steps             = models.PositiveIntegerField(default=0, help_text="Steps counted")
    intensity         = models.IntegerField(choices=INTENSITY_CHOICES, default=5)
    avg_bpm = models.FloatField(null=True, blank=True, 
                             help_text="Average heart rate during workout (optional)")
    calories_predicted= models.FloatField(null=True, blank=True)
    date              = models.DateField(auto_now_add=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.user.username} — {self.workout_type} ({self.date})"
