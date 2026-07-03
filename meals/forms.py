"""
meals/forms.py
"""
from django import forms
from .models import MealLog


class MealForm(forms.ModelForm):
    class Meta:
        model  = MealLog
        fields = ['meal_name', 'meal_type', 'calories', 'protein', 'carbs', 'fats']
        widgets = {
            'meal_name': forms.TextInput(attrs={'placeholder': 'e.g. Grilled Chicken with Rice'}),
            'meal_type': forms.Select(),
            'calories':  forms.NumberInput(attrs={'placeholder': 'Total calories', 'step': '0.1', 'min': 0}),
            'protein':   forms.NumberInput(attrs={'placeholder': 'Protein (g)', 'step': '0.1', 'min': 0}),
            'carbs':     forms.NumberInput(attrs={'placeholder': 'Carbs (g)', 'step': '0.1', 'min': 0}),
            'fats':      forms.NumberInput(attrs={'placeholder': 'Fats (g)', 'step': '0.1', 'min': 0}),
        }

    def clean_calories(self):
        cal = self.cleaned_data.get('calories')
        if cal is not None and cal < 0:
            raise forms.ValidationError("Calories cannot be negative.")
        return cal
