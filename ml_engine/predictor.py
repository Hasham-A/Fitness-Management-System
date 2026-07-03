
"""
ml_engine/predictor.py

Loads trained models and runs all ML inference for the fitness app.
Four functions:
    predict_calories()      — how much did you burn in that workout?
    predict_body_fat()      — what is your body fat %?
    predict_tdee()          — how many calories should you eat per day?
    get_full_plan()         — return complete workout + meal plan
"""
import os
import joblib
import numpy as np
from django.conf import settings


# ── Internal helper ───────────────────────────────────────────────────────────

def _load(filename):
    """Load a .pkl file from the ml_models directory."""
    path = os.path.join(settings.ML_MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found: {path}\n"
            f"Run:  python train_advanced_models.py"
        )
    return joblib.load(path)


# ── MET values per workout type (Metabolic Equivalent of Task) ────────────────
MET_MAP = {
    'running':      9.8,
    'cycling':      7.5,
    'swimming':     8.0,
    'walking':      3.5,
    'weightlifting':5.0,
    'yoga':         3.0,
    'hiit':        12.0,
    'other':        4.0,
}

# Map workout_type string to integer index (must match training script)
WORKOUT_TYPE_INDEX = {
    'running': 0, 'cycling': 1, 'swimming': 2, 'walking': 3,
    'weightlifting': 4, 'yoga': 5, 'hiit': 6, 'other': 7,
}

# Map activity level string to integer (used for TDEE)
ACTIVITY_INDEX = {
    'sedentary': 0,   # desk job, no exercise
    'light': 1,       # 1-3 days/week exercise
    'moderate': 2,    # 3-5 days/week exercise
    'active': 3,      # 6-7 days/week exercise
    'very_active': 4, # athlete / physical job
}


# ── 1. CALORIE BURN PREDICTION ─────────────────────────────────────────────────

def predict_calories(workout_type: str, duration: int, steps: int,
                     intensity: int, weight: float, age: int,
                     gender: str, height: float = 170.0,
                     avg_bpm: float = None) -> float:
    """
    Predict calories burned during a workout session.

    Features sent to model (exactly matches Colab training):
        Age, Height(m), Weight(kg), Session_Duration(hours), Avg_BPM, Gender_enc

    Args:
        workout_type : type of exercise
        duration     : minutes
        steps        : steps (kept for form compatibility, not used by model)
        intensity    : 1-10 scale
        weight       : kg
        age          : years
        gender       : 'M' or 'F'
        height       : cm (converted to metres inside this function)
        avg_bpm      : average heart rate — estimated from intensity if not given

    Returns:
        Predicted calories burned as float
    """
    model = _load('calorie_model.pkl')

    # Convert units to match training data
    duration_hours = duration / 60.0          # minutes → hours
    height_m       = (height or 170) / 100.0  # cm → metres

    # Gender: Male=1, Female=0
    gender_enc = 1 if gender == 'M' else 0

    # Estimate BPM from intensity if user didn't provide it
    # Intensity 1 ≈ 90 BPM (very easy), Intensity 10 ≈ 180 BPM (max effort)
    if avg_bpm is None:
        avg_bpm = 80 + (intensity * 10)

    # EXACT same feature order as training:
    # ['Age', 'Height (m)', 'Weight (kg)', 'Session_Duration (hours)', 'Avg_BPM', 'Gender_enc']
    features = np.array([[
        float(age    or 25),
        float(height_m),
        float(weight or 70),
        float(duration_hours),
        float(avg_bpm),
        float(gender_enc),
    ]])

    prediction = model.predict(features)[0]
    return round(max(float(prediction), 50), 1)


# ── 2. BODY FAT % PREDICTION ──────────────────────────────────────────────────

def predict_body_fat(age: int, weight: float, height: float,
                     gender: str, waist: float = None,
                     chest: float = None, hip: float = None,
                     thigh: float = None) -> float:
    """
    Predict body fat percentage from biometric inputs.

    Features (must match training exactly):
        Age, Weight_kg, Height_cm, Chest, BMI, Abdomen, Hip, Thigh
    
    Returns:
        Predicted body fat % (float, clamped 3–55%)
    """
    model = _load('bfp_model.pkl')

    # Calculate BMI
    bmi = weight / ((height / 100) ** 2) if height > 0 else 25.0

    # Use neutral defaults if optional measurements not provided
    chest_val = chest  if chest  else (weight * 0.6)   # rough estimate
    waist_val = waist  if waist  else (weight * 0.49)
    hip_val   = hip    if hip    else (weight * 0.61)
    thigh_val = thigh  if thigh  else (weight * 0.32)

    # Order must EXACTLY match training:
    # Age, Weight_kg, Height_cm, Chest, BMI, Abdomen(waist), Hip, Thigh
    features = np.array([[
        float(age),
        float(weight),
        float(height),
        float(chest_val),
        float(bmi),
        float(waist_val),
        float(hip_val),
        float(thigh_val),
    ]])

    prediction = model.predict(features)[0]
    return round(float(np.clip(prediction, 3.0, 55.0)), 1)


# ── 3. TDEE PREDICTION ────────────────────────────────────────────────────────

def predict_tdee(age: int, weight: float, height: float, gender: str,
                 activity_level: str, fitness_goal: str) -> int:
    """
    Predict Total Daily Energy Expenditure — how many calories to eat per day
    to meet the user's fitness goal.

    Args:
        activity_level : sedentary / light / moderate / active / very_active
        fitness_goal   : weight_loss / muscle_gain / maintenance / endurance

    Returns:
        Recommended daily calorie intake as an integer
    """
    model = _load('tdee_model.pkl')

    gender_enc   = 1 if gender == 'M' else 0
    activity_enc = ACTIVITY_INDEX.get(activity_level, 2)
    goal_enc     = {'weight_loss': 0, 'muscle_gain': 1,
                    'maintenance': 2, 'endurance': 3}.get(fitness_goal, 2)

    # BMR via Mifflin-St Jeor (same formula used in training)
    if gender == 'M':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    features = np.array([[
        float(age),
        float(weight),
        float(height),
        float(gender_enc),
        float(activity_enc),
        float(goal_enc),
        float(bmr),
    ]])

    prediction = model.predict(features)[0]
    return int(round(np.clip(prediction, 1200, 5000)))


# ── 4. FULL PERSONALIZED PLAN ─────────────────────────────────────────────────

def get_full_plan(fitness_goal: str, experience_level: str,
                  age: int, weight: float, height: float,
                  gender: str, activity_level: str) -> dict:
    """
    Return a complete, structured workout + meal plan for the user.

    Args:
        fitness_goal     : weight_loss / muscle_gain / maintenance / endurance
        experience_level : beginner / intermediate
        activity_level   : sedentary / light / moderate / active / very_active

    Returns:
        A dictionary containing:
            tdee              — recommended daily calories (int)
            workout_days      — how many days per week to train (int)
            workout_schedule  — list of daily exercise plans with sets/reps
            rest_days_note    — guidance for rest days
            meal_principles   — list of nutrition rules
            meal_plan         — structured daily meals with foods and quantities
            daily_totals      — approximate macro summary
            weekly_note       — weekly tracking advice
            macros            — recommended protein/carb/fat breakdown
    """
    db = _load('plan_database.pkl')
    workout_plans = db['workout_plans']
    meal_plans    = db['meal_plans']

    # Normalise inputs
    goal  = fitness_goal     if fitness_goal     in workout_plans else 'maintenance'
    level = experience_level if experience_level in ('beginner', 'intermediate') else 'beginner'

    # Get TDEE from ML model
    tdee = predict_tdee(age, weight, height, gender, activity_level, goal)

    # Pull the right workout plan
    workout_data = workout_plans[goal][level]

    # Pull the right meal plan
    meal_data = meal_plans[goal]

    # Calculate personal macro targets
    protein_g = round(weight * 1.8)                          # 1.8g per kg bodyweight
    fat_g     = round((tdee * 0.25) / 9)                     # 25% of calories from fat
    carb_g    = round((tdee - (protein_g * 4) - (fat_g * 9)) / 4)  # remainder from carbs
    carb_g    = max(carb_g, 50)                              # minimum 50g carbs

    return {
        'tdee':             tdee,
        'fitness_goal':     goal,
        'experience_level': level,
        'workout_days':     workout_data['workout_days'],
        'workout_schedule': workout_data['workout_schedule'],
        'rest_days_note':   workout_data['rest_days_note'],
        'meal_principles':  meal_data['principles'],
        'meal_plan':        meal_data['daily_plan'],
        'daily_totals':     meal_data['daily_total'],
        'weekly_note':      meal_data['weekly_note'],
        'macros': {
            'calories': tdee,
            'protein':  protein_g,
            'carbs':    carb_g,
            'fat':      fat_g,
        },
    }
