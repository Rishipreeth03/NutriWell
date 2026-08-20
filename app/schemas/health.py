from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime


class HealthAssessmentCreate(BaseModel):
    user_id: int

    age: int = Field(ge=1, le=120)
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)

    sleep_hours: float = Field(ge=0, le=24)
    exercise_minutes: int = Field(ge=0)
    water_liters: float = Field(ge=0)

    stress_level: int = Field(ge=1, le=10)
    diet_quality: int = Field(ge=1, le=10)


class HealthAssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    age: int
    height_cm: float
    weight_kg: float

    sleep_hours: float
    exercise_minutes: int
    water_liters: float

    stress_level: int
    diet_quality: int

    wellbeing_score: float | None
    risk_level: str | None

    created_at: datetime