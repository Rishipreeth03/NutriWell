from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from app.models.ml_model import get_model
from app.schemas.health import PredictRequest

MODEL_FEATURE_ORDER = [
    "Age",
    "BMI",
    "Exercise_Frequency",
    "Diet_Quality",
    "Sleep_Hours",
    "Smoking_Status",
    "Alcohol_Consumption",
]


def prepare_model_input(data: PredictRequest) -> pd.DataFrame:
    feature_row = {
        "Age": float(data.age),
        "BMI": float(data.bmi),
        "Exercise_Frequency": float(data.exercise_frequency),
        "Diet_Quality": float(data.diet_quality),
        "Sleep_Hours": float(data.sleep_hours),
        "Smoking_Status": float(data.smoking_status),
        "Alcohol_Consumption": float(data.alcohol_consumption),
    }

    return pd.DataFrame([feature_row], columns=MODEL_FEATURE_ORDER)


def normalize_prediction(raw_prediction: Any) -> float:
    if isinstance(raw_prediction, np.ndarray):
        value = raw_prediction.item()
    elif isinstance(raw_prediction, (list, tuple)):
        value = raw_prediction[0]
    else:
        value = raw_prediction

    if hasattr(value, "item"):
        value = value.item()

    value = float(value)
    return max(0.0, min(100.0, value))


def predict_health(data: PredictRequest) -> float:
    model = get_model()
    feature_frame = prepare_model_input(data)

    try:
        prediction = model.predict(feature_frame)
    except Exception as exc:  # pragma: no cover - runtime guard
        raise RuntimeError("The ML model could not generate a prediction.") from exc

    return normalize_prediction(prediction)
