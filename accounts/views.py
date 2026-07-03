"""
accounts/views.py
Handles registration, login, logout, and profile management.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import UserProfile


def register_view(request):
    """Show registration form and create a new user + profile."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        # Automatically create a blank profile for this user
        UserProfile.objects.create(user=user)
        messages.success(request, "Account created! Please log in.")
        return redirect('accounts:login')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Authenticate and log in a user."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard:home')
        else:
            error = "Invalid username or password. Please try again."

    return render(request, 'accounts/login.html', {'error': error})


@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Display and update the user's fitness profile."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard:home')

    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
    })
