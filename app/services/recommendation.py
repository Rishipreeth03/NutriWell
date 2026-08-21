from __future__ import annotations

from app.schemas.health import PredictRequest


def classify_risk(score: float) -> str:
    if score >= 70:
        return "Low"
    if score >= 40:
        return "Moderate"
    return "High"


def build_recommendations(prediction: float | None, data: PredictRequest) -> list[str]:
    risk_level = classify_risk(float(prediction or 0))

    if risk_level == "Low":
        return [
            "Maintain your current sleep and nutrition routine.",
            "Keep regular physical activity and aim for balanced meals.",
        ]

    if risk_level == "Moderate":
        return [
            "Improve your sleep consistency and daily movement.",
            "Focus on balanced meals and reducing excess alcohol or smoking exposure.",
        ]

    return [
        "Increase sleep quality and physical activity gradually.",
        "Prioritize a nutrient-dense diet and reduce high-risk habits for better health.",
    ]
