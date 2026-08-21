from pathlib import Path
from typing import Any

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATHS = [
    PROJECT_ROOT / "models" / "model_prediction.pkl",
    PROJECT_ROOT / "models" / "model_predict.pkl",
]
_model: Any | None = None


def load_model() -> Any:
    global _model

    if _model is not None:
        return _model

    for candidate in MODEL_PATHS:
        if candidate.exists():
            try:
                _model = joblib.load(candidate)
                return _model
            except Exception as exc:  # pragma: no cover - defensive guard
                raise RuntimeError(
                    f"Failed to load the ML model from {candidate}."
                ) from exc

    raise FileNotFoundError(
        "The ML model file was not found. Expected one of: "
        + ", ".join(str(path) for path in MODEL_PATHS)
        + ". Run the training scripts in ml/ to generate the pickle."
    )


def get_model() -> Any:
    return load_model()
