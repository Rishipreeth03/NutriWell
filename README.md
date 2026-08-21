# NutriWell

NutriWell is a FastAPI + SQLAlchemy + Streamlit/Gradio project for health prediction and recommendations.

## Prerequisites

- Python 3.14+
- Poetry
- MySQL server running locally

## Setup

1. Install dependencies:
   `poetry install`
2. Copy the sample environment values or create a `.env` file with:
   `DATABASE_URL=mysql+pymysql://username:password@localhost:3306/nutriwell`
   `API_URL=http://localhost:8000`

## Database migration

Run:

`poetry run alembic upgrade head`

If a migration is needed for a schema change, generate it with:

`poetry run alembic revision --autogenerate -m "create health records"`

## Run the backend

`poetry run uvicorn app.main:app --reload`

Open `/docs` in the browser.

## Run the frontend

`poetry run gradio run frontend/app.py`

## Run tests

`poetry run pytest`

## Model status

The project expects a pre-trained model at `models/model_prediction.pkl`.
This file is treated as read-only. The repository currently does not contain it, so the prediction service raises a clear error until the ML artifact is provided.

## API

POST `/api/predict`

Request body:

```json
{
  "email": "user@gmail.com",
  "age": 30,
  "bmi": 22.5,
  "sleep_hours": 7.5,
  "exercise_days": 4,
  "stress_level": 3,
  "water_intake": 2.1
}
```

Response body:

```json
{
  "email": "user@gmail.com",
  "prediction": "Good",
  "recommendations": [
    "Maintain your current sleep and nutrition routine.",
    "Keep regular physical activity and aim for balanced meals."
  ],
  "created_at": "2026-08-21T00:00:00"
}
```

## Important note

The exact ML feature order and preprocessing cannot be verified from the repository because `ml/train.py`, `ml/preprocess.py`, and the model pickle are not present. The project handles this by failing with a clear message instead of guessing or modifying the model.

```json
{
http://127.0.0.1:7860 frontend ports
http://localhost:8000/docs  backend ports
}
```