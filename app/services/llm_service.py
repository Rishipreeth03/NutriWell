import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in .env"
    )


client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_wellness_response(
    age: int,
    height_cm: float,
    weight_kg: float,
    sleep_hours: float,
    exercise_minutes: int,
    water_liters: float,
    stress_level: int,
    diet_quality: int,
    wellbeing_score: float | None,
    risk_level: str | None,
    recommended_meals: list[str],
) -> str:

    prompt = f"""
You are NutriWell, a friendly nutrition and wellbeing assistant.

Your job is to explain a user's wellbeing assessment and provide
practical, general wellness suggestions.

IMPORTANT:
- Do not diagnose diseases.
- Do not claim to replace a doctor or dietitian.
- Do not prescribe medication.
- Do not invent health information.
- Base your response only on the information provided.
- Keep the advice practical and easy to understand.

User information:
- Age: {age}
- Height: {height_cm} cm
- Weight: {weight_kg} kg
- Sleep: {sleep_hours} hours/night
- Exercise: {exercise_minutes} minutes
- Water intake: {water_liters} liters/day
- Stress level: {stress_level}/10
- Diet quality: {diet_quality}/10

NutriWell assessment:
- Wellbeing score: {wellbeing_score}
- Risk level: {risk_level}

Recommended meals:
{", ".join(recommended_meals)}

Generate a concise response with these sections:

1. Wellbeing Summary
2. What You Are Doing Well
3. Areas to Improve
4. Meal Suggestions
5. One Simple Goal for Today

Use a supportive and non-judgmental tone.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text