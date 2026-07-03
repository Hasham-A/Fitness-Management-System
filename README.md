# AI-Powered Fitness Management System

A full-stack web application that integrates machine learning models 
to deliver intelligent fitness tracking and personalised health recommendations.

## Features

- Workout logging with AI-predicted calorie burn
- Body fat percentage prediction from biometric measurements
- Personalised workout and meal plan recommendations
- Interactive dashboard with Chart.js analytics
- Admin panel for user and model management

## Tech Stack

- **Backend:** Django 4.x, Python 3.10+
- **Database:** PostgreSQL
- **Machine Learning:** Scikit-learn (Random Forest, Gradient Boosting, Decision Tree)
- **Frontend:** HTML, CSS, Bootstrap 5, Chart.js
- **Deployment:** Railway

## ML Models

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Calorie Burn | Random Forest Regressor | Predicts calories burned per session |
| Body Fat % | Gradient Boosting Regressor | Estimates body fat from measurements |
| Recommendation | Decision Tree Classifier | Assigns personalised fitness plan |
| TDEE | Random Forest Regressor | Calculates daily calorie target |

## Setup Instructions

1. Clone the repository
git clone https://github.com/YOURUSERNAME/fitness-app.git
cd fitness-app

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Create a `.env` file with your settings
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://fitness_user:fitness123@localhost:5432/fitness_db

5. Run migrations and train models
python manage.py migrate
python train_advanced_models.py

6. Start the server
python manage.py runserver

## Developer

**Hasham Amar** — BS Computer Science, Islamia University of Bahawalpur (2022–2026)