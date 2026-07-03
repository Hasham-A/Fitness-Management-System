"""
accounts/forms.py
Forms for registration, login, and profile editing.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    """User registration form — collects username, email, and password."""
    password  = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }), label="Confirm Password")

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username':   forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    """Form to update a user's fitness profile."""
    class Meta:
        model  = UserProfile
        fields = ['age', 'height', 'weight', 'gender', 'fitness_goal', 
          'waist', 'chest', 'hip', 'thigh', 'activity_level', 'experience_level']
        widgets = {
            'age':          forms.NumberInput(attrs={
                'placeholder': 'Age (years)',
                'min': 1,
                'max': 120,
                'class': 'form-control',
            }),
            'height':       forms.NumberInput(attrs={
                'placeholder': 'Height (cm)',
                'step': '0.1',
                'class': 'form-control',
            }),
            'weight':       forms.NumberInput(attrs={
                'placeholder': 'Weight (kg)',
                'step': '0.1',
                'class': 'form-control',
            }),
            'gender':       forms.Select(attrs={'class': 'form-select'}),
            'fitness_goal': forms.Select(attrs={'class': 'form-select'}),
            'waist':        forms.NumberInput(attrs={
                'placeholder': 'Waist (cm)',
                'step': '0.1',
                'class': 'form-control',
            }),
            'chest':        forms.NumberInput(attrs={
                'placeholder': 'Chest (cm)',
                'step': '0.1',
                'class': 'form-control',
            }),
            'hip':          forms.NumberInput(attrs={
                'placeholder': 'Hip (cm)',
                'step': '0.1',
                'class': 'form-control',
            }),
            'thigh':        forms.NumberInput(attrs={
                'placeholder': 'Thigh (cm)',
                'step': '0.1',
                'class': 'form-control',
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 1 or age > 120):
            raise forms.ValidationError("Please enter a valid age between 1 and 120.")
        return age

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and (height < 50 or height > 300):
            raise forms.ValidationError("Please enter a valid height between 50 and 300 cm.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and (weight < 10 or weight > 500):
            raise forms.ValidationError("Please enter a valid weight between 10 and 500 kg.")
        return weight

    def clean_waist(self):
        waist = self.cleaned_data.get('waist')
        if waist is not None and (waist < 30 or waist > 200):
            raise forms.ValidationError("Please enter a valid waist circumference between 30 and 200 cm.")
        return waist

    def clean_chest(self):
        chest = self.cleaned_data.get('chest')
        if chest is not None and (chest < 50 or chest > 200):
            raise forms.ValidationError("Please enter a valid chest circumference between 50 and 200 cm.")
        return chest

    def clean_hip(self):
        hip = self.cleaned_data.get('hip')
        if hip is not None and (hip < 50 or hip > 200):
            raise forms.ValidationError("Please enter a valid hip circumference between 50 and 200 cm.")
        return hip

    def clean_thigh(self):
        thigh = self.cleaned_data.get('thigh')
        if thigh is not None and (thigh < 30 or thigh > 150):
            raise forms.ValidationError("Please enter a valid thigh circumference between 30 and 150 cm.")
        return thigh
