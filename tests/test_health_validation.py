import pytest
from pydantic import ValidationError

from app.schemas.health import PredictRequest


def test_predict_request_requires_valid_email():
    with pytest.raises(ValidationError):
        PredictRequest(
            email="not-an-email",
            age=30,
            bmi=22.5,
            sleep_hours=7.5,
        )


def test_predict_request_accepts_core_fields():
    payload = PredictRequest(
        email="user@example.com",
        age=30,
        bmi=22.5,
        exercise_frequency=4,
        diet_quality=80,
        sleep_hours=7.5,
        smoking_status=0,
        alcohol_consumption=1.5,
    )

    assert payload.email == "user@example.com"  # nosec B101
    assert payload.age == 30  # nosec B101
    assert payload.bmi == 22.5  # nosec B101
    assert payload.exercise_frequency == 4  # nosec B101
    assert payload.diet_quality == 80  # nosec B101
    assert payload.sleep_hours == 7.5  # nosec B101
