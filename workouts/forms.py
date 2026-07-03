"""
workouts/forms.py
"""
from django import forms
from .models import WorkoutLog


class WorkoutForm(forms.ModelForm):
    class Meta:
        model  = WorkoutLog
        fields = ['workout_type', 'duration', 'steps', 'intensity', 'avg_bpm']
        widgets = {
    # ... existing widgets ...
    'avg_bpm': forms.NumberInput(attrs={
        'placeholder': 'Avg Heart Rate BPM — optional', 
        'min': 60, 'max': 220
    }),
}
        labels = {
            'duration':  'Duration (minutes)',
            'steps':     'Steps Taken',
            'intensity': 'Intensity Level (1=Easy, 10=Max)',
        }

    def clean_duration(self):
        d = self.cleaned_data.get('duration')
        if d is not None and d < 1:
            raise forms.ValidationError("Duration must be at least 1 minute.")
        return d
