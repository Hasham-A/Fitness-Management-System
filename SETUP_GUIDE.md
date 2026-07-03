# AI Fitness Management System — Setup Guide (Windows)

## PHASE 1: Project Setup

### Step 1 — Create project folder
Open Command Prompt and run:
```
mkdir fitness_project
cd fitness_project
```

### Step 2 — Create and activate virtual environment
```
python -m venv venv
venv\Scripts\activate
```
You should see `(venv)` in your terminal.

### Step 3 — Install all dependencies
```
pip install django psycopg2-binary scikit-learn pandas numpy joblib Pillow
```

### Step 4 — Create Django project and apps
```
django-admin startproject core .
python manage.py startapp accounts
python manage.py startapp workouts
python manage.py startapp meals
python manage.py startapp dashboard
python manage.py startapp recommendations
```

## PHASE 2 — Copy the project files
Copy every file from this folder into the corresponding locations.

## PHASE 3 — PostgreSQL Setup
Open pgAdmin or psql and run:
```sql
CREATE DATABASE fitness_db;
CREATE USER fitness_user WITH PASSWORD 'fitness123';
GRANT ALL PRIVILEGES ON DATABASE fitness_db TO fitness_user;
```

## PHASE 4 — Run Migrations and Train Models
```
python manage.py makemigrations
python manage.py migrate
python manage.py train_models
python manage.py createsuperuser
```

## PHASE 5 — Start the Server
```
python manage.py runserver
```
Visit: http://127.0.0.1:8000
