"""
meals/views.py
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MealForm
from .models import MealLog


@login_required
def log_meal(request):
    form = MealForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        meal = form.save(commit=False)
        meal.user = request.user
        meal.save()
        messages.success(request, f"Meal '{meal.meal_name}' logged successfully!")
        return redirect('meals:history')
    return render(request, 'meals/log_meal.html', {'form': form})


@login_required
def update_meal(request, pk):
    meal = get_object_or_404(MealLog, pk=pk, user=request.user)
    form = MealForm(request.POST or None, instance=meal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Meal '{meal.meal_name}' updated successfully!")
        return redirect('meals:history')
    return render(request, 'meals/log_meal.html', {
        'form': form,
        'meal': meal,
        'is_update': True,
    })


@login_required
def delete_meal(request, pk):
    meal = get_object_or_404(MealLog, pk=pk, user=request.user)
    if request.method == 'POST':
        meal_name = meal.meal_name
        meal.delete()
        messages.success(request, f"Meal '{meal_name}' deleted successfully.")
        return redirect('meals:history')
    return render(request, 'meals/delete_meal.html', {'meal': meal})


@login_required
def meal_history(request):
    meals = MealLog.objects.filter(user=request.user)
    return render(request, 'meals/history.html', {'meals': meals})
