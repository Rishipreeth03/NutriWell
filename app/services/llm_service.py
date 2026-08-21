from __future__ import annotations

import json
import logging

from google import genai
from google.genai import types

from app.config import settings
from app.schemas.health import GeminiRecommendations, PredictRequest

logger = logging.getLogger(__name__)
MODEL_NAME = "gemini-2.5-flash"


def fallback_recommendations() -> GeminiRecommendations:
    return GeminiRecommendations(
        food=[
            "Build meals around vegetables, fruit, whole grains, and protein.",
            "Choose water more often and limit highly processed snacks.",
            "Plan regular meals with portions that fit your activity level.",
        ],
        lifestyle=[
            "Aim for a consistent sleep schedule.",
            "Add regular movement that feels manageable.",
            "Reduce smoking and excess alcohol where applicable.",
        ],
        priority="Focus on one sustainable daily habit this week.",
        message="Small, consistent choices can make a meaningful difference.",
    )


def get_gemini_recommendations(
    data: PredictRequest,
    health_score: float,
    risk_level: str,
) -> GeminiRecommendations:
    """Return short non-diagnostic recommendations, with a safe local fallback."""
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not configured; using fallback recommendations.")
        return fallback_recommendations()

    health_context = {
        "age": data.age,
        "bmi": data.bmi,
        "exercise_frequency_days_per_week": data.exercise_frequency,
        "diet_quality_score": data.diet_quality,
        "sleep_hours": data.sleep_hours,
        "smoking_status": data.smoking_status,
        "alcohol_consumption": data.alcohol_consumption,
        "ml_health_score": round(health_score, 2),
        "ml_risk_level": risk_level,
    }
    prompt = (
        "Give concise, personalized general wellness recommendations from this "
        "health context. The ML health score and risk level are already calculated; "
        "do not recalculate or challenge them. Do not diagnose diseases or prescribe "
        "medication. Return exactly three food recommendations, exactly three lifestyle "
        "recommendations, one priority, and one brief encouraging message. Return only "
        "JSON in this exact shape: {\"food\":[\"...\",\"...\",\"...\"],"
        "\"lifestyle\":[\"...\",\"...\",\"...\"],\"priority\":\"...\","
        "\"message\":\"...\"}. "
        f"Health context: {json.dumps(health_context)}"
    )

    try:
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=10_000),
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=400,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        if not response.text:
            raise ValueError("Gemini returned no recommendation content.")
        return GeminiRecommendations.model_validate_json(response.text)
    except Exception:
        logger.exception("Gemini recommendations failed; using fallback recommendations.")
        return fallback_recommendations()
