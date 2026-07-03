"""
workouts/views.py
Handles workout logging and calorie prediction.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WorkoutForm
from .models import WorkoutLog
from ml_engine.predictor import predict_calories


def _predict_calories_for_workout(workout, request):
    profile = getattr(request.user, 'profile', None)
    weight  = profile.weight if profile else 70
    age     = profile.age    if profile else 25
    gender  = profile.gender if profile else 'M'
    predicted_calories = None

    try:
        predicted_calories = predict_calories(
    workout_type = workout.workout_type,
    duration     = workout.duration,
    steps        = workout.steps,
    intensity    = workout.intensity,
    weight       = weight,
    age          = age,
    gender       = gender,
    height       = profile.height if profile else 170.0,
    avg_bpm      = workout.avg_bpm,   # None if not entered, function handles it
)
        workout.calories_predicted = predicted_calories
    except FileNotFoundError as e:
        messages.warning(request, f"ML model unavailable: {e}")

    return predicted_calories


@login_required
def log_workout(request):
    """Show the workout form; on submission call the calorie ML model."""
    form = WorkoutForm(request.POST or None)
    predicted_calories = None

    if request.method == 'POST' and form.is_valid():
        workout = form.save(commit=False)
        workout.user = request.user
        predicted_calories = _predict_calories_for_workout(workout, request)
        workout.save()
        messages.success(request, f"Workout logged! Estimated calories burned: {predicted_calories or 'N/A'}")
        return redirect('workouts:history')

    return render(request, 'workouts/log_workout.html', {
        'form': form,
        'predicted_calories': predicted_calories,
    })


@login_required
def update_workout(request, pk):
    workout = get_object_or_404(WorkoutLog, pk=pk, user=request.user)
    form = WorkoutForm(request.POST or None, instance=workout)
    predicted_calories = workout.calories_predicted

    if request.method == 'POST' and form.is_valid():
        workout = form.save(commit=False)
        workout.user = request.user
        predicted_calories = _predict_calories_for_workout(workout, request)
        workout.save()
        messages.success(request, f"Workout updated! Estimated calories burned: {predicted_calories or 'N/A'}")
        return redirect('workouts:history')

    return render(request, 'workouts/log_workout.html', {
        'form': form,
        'predicted_calories': predicted_calories,
        'workout': workout,
        'is_update': True,
    })


@login_required
def delete_workout(request, pk):
    workout = get_object_or_404(WorkoutLog, pk=pk, user=request.user)
    if request.method == 'POST':
        workout_type = workout.workout_type
        workout.delete()
        messages.success(request, f"Workout '{workout_type}' deleted successfully.")
        return redirect('workouts:history')
    return render(request, 'workouts/delete_workout.html', {'workout': workout})


@login_required
def workout_history(request):
    """Show all workouts for the logged-in user."""
    workouts = WorkoutLog.objects.filter(user=request.user)
    return render(request, 'workouts/history.html', {'workouts': workouts})
