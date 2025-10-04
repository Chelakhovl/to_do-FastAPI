# FastAPI To-Do + Celery/Redis + ML `/predict`

A clean, production-ready FastAPI project that implements:

- **Task 1:** REST API for a to-do list  
  In-memory storage, Pydantic v2 validation, unit tests.
- **Task 2:** Automation job that fetches users from a public API and saves a CSV  
  Celery worker + Beat scheduler, Redis broker, Docker Compose.
- **Task 3 (optional):** Simple ML integration  
  Train TF-IDF + LogisticRegression on a CSV; expose `/predict` to classify task priority (`high|low`).

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start (Docker)](#quick-start-docker)
- [Local Development (no Docker)](#local-development-no-docker)

---

## Features

- Clean architecture (API ↔ Services ↔ Repositories ↔ Core)
- Thread-safe in-memory storage for tasks
- Pydantic v2 models & validation
- Centralized error handling
- Celery worker + Beat with Redis broker
- HTTP client via `httpx` to fetch users → CSV (`data/users.csv`)
- Simple ML model (TF-IDF + LogisticRegression) with lazy loading and `/predict`
- Fully containerized with Docker Compose
- Pytest unit tests

---

## Tech Stack

- **FastAPI**, **Uvicorn**
- **Pydantic v2**, **pydantic-settings**
- **Celery 5**, **Redis**
- **httpx**
- **scikit-learn**, **joblib**
- **Pytest**
- **Docker / Docker Compose**
- **Black** (formatting)

---

## Commands

```bash
# 1) Clone
git clone https://github.com/Chelakhovl/to_do-FastAPI.git
cd to_do-FastAPI

## Local run with virtualenv + environment variables

```bash
# 1) Create venv and install deps
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt


# 2) Create a file named ".env"
APP_NAME="To-Do API"
DEBUG=True
TIMEZONE="Europe/Kyiv"

# Redis/Celery
REDIS_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# CSV job settings
USERS_URL="https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR="./data"

# ML model path
MODEL_PATH="models/task_priority_model.joblib"

# 3) Run API
python -m uvicorn app.main:app --reload
# -> http://127.0.0.1:8000


# 3) Docker Compose (API + Redis + Celery worker + Beat)
docker compose up --build
# API -> http://localhost:8000



Swagger UI: http://localhost:8000/docs
OpenAPI JSON: http://localhost:8000/openapi.json