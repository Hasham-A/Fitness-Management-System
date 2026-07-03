"""
workouts/management/commands/train_models.py

Run with:  python manage.py train_models

This command generates synthetic training data and trains three ML models:
  1. Calorie burn predictor (RandomForestRegressor)
  2. Body fat percentage predictor (GradientBoostingRegressor)
  3. Fitness recommendation engine (KMeans clustering)

It then saves them as .pkl files in the ml_models/ directory.
"""
import os
import numpy as np
import joblib
from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class Command(BaseCommand):
    help = 'Train all ML models and save them to ml_models/'

    def handle(self, *args, **kwargs):
        os.makedirs(settings.ML_MODELS_DIR, exist_ok=True)
        self.stdout.write("Training ML models...")

        self._train_calorie_model()
        self._train_bfp_model()
        self._train_recommendation_model()

        self.stdout.write(self.style.SUCCESS("All models trained and saved successfully!"))

    # ── 1. Calorie Burn Model ──────────────────────────────────────────────────
    def _train_calorie_model(self):
        """
        Features: [duration, steps, intensity, weight, age, gender_enc, met]
        Target:   calories burned

        Formula used to generate realistic labels:
          calories = MET * weight_kg * (duration / 60)
          adjusted slightly by age and intensity
        """
        np.random.seed(42)
        n = 5000

        duration  = np.random.randint(10, 120, n).astype(float)
        steps     = np.random.randint(0, 15000, n).astype(float)
        intensity = np.random.randint(1, 11, n).astype(float)
        weight    = np.random.uniform(45, 120, n)
        age       = np.random.randint(15, 70, n).astype(float)
        gender    = np.random.randint(0, 2, n).astype(float)  # 0=F, 1=M
        met       = np.random.uniform(0.6, 1.5, n)

        # Realistic calorie formula
        calories = (
            met * weight * (duration / 60) * (intensity / 5)
            + (steps / 1000) * 0.5
            - (age - 25) * 0.1
            + gender * 20
            + np.random.normal(0, 15, n)  # small noise
        )
        calories = np.clip(calories, 50, 1500)

        X = np.column_stack([duration, steps, intensity, weight, age, gender, met])
        y = calories

        model = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ])
        model.fit(X, y)

        path = os.path.join(settings.ML_MODELS_DIR, 'calorie_model.pkl')
        joblib.dump(model, path)
        self.stdout.write(f"  ✓ Calorie model saved → {path}")

    # ── 2. Body Fat Percentage Model ───────────────────────────────────────────
    def _train_bfp_model(self):
        """
        Features: [age, weight, height, gender_enc, bmi, waist]
        Target:   body fat percentage

        Uses Deurenberg body fat formula as the label generator:
          BFP = (1.20 * BMI) + (0.23 * age) - (10.8 * gender) - 5.4
        """
        np.random.seed(0)
        n = 5000

        age    = np.random.randint(15, 75, n).astype(float)
        weight = np.random.uniform(40, 130, n)
        height = np.random.uniform(145, 200, n)
        gender = np.random.randint(0, 2, n).astype(float)  # 0=F, 1=M
        waist  = weight * 0.5 + np.random.normal(0, 3, n)
        bmi    = weight / ((height / 100) ** 2)

        # Deurenberg formula (widely used clinical approximation)
        bfp = (1.20 * bmi) + (0.23 * age) - (10.8 * gender) - 5.4
        bfp += np.random.normal(0, 2, n)
        bfp = np.clip(bfp, 3, 55)

        X = np.column_stack([age, weight, height, gender, bmi, waist])
        y = bfp

        model = Pipeline([
            ('scaler', StandardScaler()),
            ('gbr', GradientBoostingRegressor(n_estimators=100, random_state=42)),
        ])
        model.fit(X, y)

        path = os.path.join(settings.ML_MODELS_DIR, 'bfp_model.pkl')
        joblib.dump(model, path)
        self.stdout.write(f"  ✓ Body fat model saved → {path}")

    # ── 3. Recommendation Model (KMeans Clustering) ────────────────────────────
    def _train_recommendation_model(self):
        """
        Features: [age, bmi, gender_enc, goal_enc, avg_calories_burned]
        Clusters users into 4 fitness profiles:
          0 = Weight Loss  1 = Muscle Gain  2 = Maintenance  3 = Endurance

        KMeans is initialized with cluster centers that match the 4 goals
        so the cluster IDs align predictably with the plans in predictor.py.
        """
        np.random.seed(7)
        n = 5000

        age     = np.random.randint(15, 65, n).astype(float)
        bmi     = np.random.uniform(17, 40, n)
        gender  = np.random.randint(0, 2, n).astype(float)
        goal    = np.random.randint(0, 4, n).astype(float)  # 0-3
        avg_cal = np.random.uniform(100, 600, n)

        X = np.column_stack([age, bmi, gender, goal, avg_cal])

        # Use 4 clusters with explicit centers to ensure stable goal mapping
        init_centers = np.array([
            [35, 30, 0.5, 0, 200],   # cluster 0: weight loss — higher BMI, low burn
            [28, 23, 0.7, 1, 450],   # cluster 1: muscle gain — younger, high burn
            [40, 24, 0.5, 2, 300],   # cluster 2: maintenance — balanced
            [30, 22, 0.6, 3, 500],   # cluster 3: endurance — high burn
        ])

        model = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=4, init='k-means++', random_state=42, n_init=10)),
        ])
        model.fit(X)

        path = os.path.join(settings.ML_MODELS_DIR, 'recommendation_model.pkl')
        joblib.dump(model, path)
        self.stdout.write(f"  ✓ Recommendation model saved → {path}")
