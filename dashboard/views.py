"""
dashboard/views.py

The main analytics hub. Aggregates workout and meal data,
prepares JSON for Chart.js, and shows summary statistics.
"""
import json
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from workouts.models import WorkoutLog
from meals.models import MealLog
from accounts.models import UserProfile
from ml_engine.predictor import predict_body_fat


@login_required
def home(request):
    """Main dashboard — summary cards + Chart.js charts."""
    user    = request.user
    today   = date.today()
    day30   = today - timedelta(days=30)

    # ── Recent workout data ──────────────────────────────────
    workouts_30 = WorkoutLog.objects.filter(user=user, date__gte=day30).order_by('date')
    total_workouts  = workouts_30.count()
    total_calories  = workouts_30.aggregate(s=Sum('calories_predicted'))['s'] or 0
    total_steps     = workouts_30.aggregate(s=Sum('steps'))['s'] or 0

    # ── Recent meal data ─────────────────────────────────────
    meals_30        = MealLog.objects.filter(user=user, date__gte=day30).order_by('date')
    total_intake    = meals_30.aggregate(s=Sum('calories'))['s'] or 0

    # ── Chart: daily calories burned (last 14 days) ──────────
    labels_burn, data_burn = _daily_series(
        WorkoutLog.objects.filter(user=user, date__gte=today - timedelta(days=14)),
        today, 14, 'calories_predicted'
    )

    # ── Chart: daily calorie intake (last 14 days) ───────────
    labels_intake, data_intake = _daily_series(
        MealLog.objects.filter(user=user, date__gte=today - timedelta(days=14)),
        today, 14, 'calories'
    )

    # ── Chart: steps per day (last 14 days) ──────────────────
    _, data_steps = _daily_series(
        WorkoutLog.objects.filter(user=user, date__gte=today - timedelta(days=14)),
        today, 14, 'steps'
    )

    # ── Body fat prediction (if profile is complete) ─────────
    bfp = None
    profile = getattr(user, 'profile', None)
    if profile and profile.age and profile.weight and profile.height and profile.gender and profile.waist and profile.chest and profile.hip and profile.thigh:
        try:
            bfp = predict_body_fat(
                age=profile.age, weight=profile.weight,
                height=profile.height, gender=profile.gender,
                waist=profile.waist, chest=profile.chest,
                hip=profile.hip, thigh=profile.thigh
            )
        except FileNotFoundError:
            pass

    return render(request, 'dashboard/home.html', {
        'total_workouts':  total_workouts,
        'total_calories':  round(total_calories, 1),
        'total_steps':     total_steps,
        'total_intake':    round(total_intake, 1),
        'net_calories':    round(total_intake - total_calories, 1),
        'bfp':             bfp,
        'profile':         profile,
        # JSON for Chart.js — must be serialized here
        'labels_json':       json.dumps(labels_burn),
        'data_burn_json':    json.dumps(data_burn),
        'data_intake_json':  json.dumps(data_intake),
        'data_steps_json':   json.dumps(data_steps),
    })


def _daily_series(queryset, today, days, field):
    """
    Build two parallel lists (labels, values) for Chart.js.
    One entry per day over the last `days` days.
    Days with no data get a 0.
    """
    # Aggregate totals by date
    from django.db.models import Sum
    daily = {
        str(row['date']): row['total']
        for row in queryset.values('date').annotate(total=Sum(field))
    }

    labels, values = [], []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime('%b %d'))
        values.append(round(daily.get(str(d), 0), 1))

    return labels, values
