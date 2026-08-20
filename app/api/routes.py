from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.database_models import (
    HealthAssessment,
    User,
)
from app.schemas.health import (
    HealthAssessmentCreate,
    HealthAssessmentResponse,
    UserCreate,
    UserResponse,
)


router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to NutriWell API"
    }


@router.post("/users", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.post(
    "/assessments",
    response_model=HealthAssessmentResponse,
)
def create_assessment(
    assessment_data: HealthAssessmentCreate,
    db: Session = Depends(get_db),
):
    user = db.get(User, assessment_data.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    assessment = HealthAssessment(
        user_id=assessment_data.user_id,
        age=assessment_data.age,
        height_cm=assessment_data.height_cm,
        weight_kg=assessment_data.weight_kg,
        sleep_hours=assessment_data.sleep_hours,
        exercise_minutes=assessment_data.exercise_minutes,
        water_liters=assessment_data.water_liters,
        stress_level=assessment_data.stress_level,
        diet_quality=assessment_data.diet_quality,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


@router.get(
    "/assessments/{assessment_id}",
    response_model=HealthAssessmentResponse,
)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assessment = db.get(
        HealthAssessment,
        assessment_id,
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return assessment