from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ml_engine.predictor import get_full_plan


@login_required
def recommendation_view(request):
    user    = request.user
    profile = getattr(user, 'profile', None)
    plan    = None
    error   = None

    required = ['age', 'weight', 'height', 'gender']
    if not profile or not all([getattr(profile, f) for f in required]):
        error = "Please complete your profile (age, weight, height, gender) first."
    else:
        try:
            plan = get_full_plan(
                fitness_goal     = profile.fitness_goal,
                experience_level = profile.experience_level,
                age              = profile.age,
                weight           = profile.weight,
                height           = profile.height,
                gender           = profile.gender,
                activity_level   = profile.activity_level,
            )
            plan['fitness_goal_display'] = profile.get_fitness_goal_display()
        except FileNotFoundError as e:
            error = f"Models not found. Run: python train_advanced_models.py"
        except Exception as e:
            error = f"Error generating plan: {e}"

    return render(request, 'recommendations/recommendation.html', {
        'plan':    plan,
        'error':   error,
        'profile': profile,
    })