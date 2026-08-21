from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.database_models import HealthRecord
from app.schemas.health import PredictRequest, PredictResponse
from app.services.prediction import predict_health
from app.services.recommendation import build_recommendations, classify_risk


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to NutriWell API"}


@router.post("/api/predict", response_model=PredictResponse)
def predict_health_record(
    payload: PredictRequest,
    db: Session = Depends(get_db),
):
    try:
        prediction = predict_health(payload)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    risk_level = classify_risk(prediction)
    recommendations = build_recommendations(prediction, payload)

    record = HealthRecord(
        email=str(payload.email),
        age=payload.age,
        bmi=payload.bmi,
        exercise_frequency=payload.exercise_frequency,
        diet_quality=payload.diet_quality,
        sleep_hours=payload.sleep_hours,
        smoking_status=payload.smoking_status,
        alcohol_consumption=payload.alcohol_consumption,
        prediction=float(prediction),
        risk_level=risk_level,
        created_at=datetime.utcnow(),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return PredictResponse(
        email=payload.email,
        prediction=float(prediction),
        risk_level=risk_level,
        recommendations=recommendations,
        created_at=record.created_at,
    )