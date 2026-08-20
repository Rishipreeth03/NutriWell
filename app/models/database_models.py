from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    assessments: Mapped[list["HealthAssessment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class HealthAssessment(Base):
    __tablename__ = "health_assessments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    height_cm: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sleep_hours: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    exercise_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    water_liters: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stress_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    diet_quality: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    wellbeing_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    risk_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="assessments",
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
    )


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    meal_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    calories: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    protein_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    carbs_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    fat_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    fiber_g: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="meal",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("health_assessments.id"),
        nullable=False,
    )

    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    llm_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    assessment: Mapped["HealthAssessment"] = relationship(
        back_populates="recommendations",
    )

    meal: Mapped["Meal"] = relationship(
        back_populates="recommendations",
    )