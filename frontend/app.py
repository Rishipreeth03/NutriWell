import json
from datetime import UTC, datetime
from pathlib import Path

import gradio as gr
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_prediction.pkl"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "predictions.json"
MODEL = joblib.load(MODEL_PATH)


def save_prediction_record(email: str, payload: dict, score: float, risk: str) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as file:
            try:
                records = json.load(file)
            except json.JSONDecodeError:
                records = []
    else:
        records = []

    records.append(
        {
            "email": email,
            "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
            "input": payload,
            "score": round(score, 2),
            "risk": risk,
        }
    )

    with DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def classify_risk(score: float) -> str:
    if score >= 70:
        return "Low"
    if score >= 40:
        return "Moderate"
    return "High"


def build_recommendations(score: float) -> str:
    risk = classify_risk(score)

    if risk == "Low":
        return (
            "Maintain your current health habits. Keep exercising regularly "
            "and eating a balanced diet."
        )

    if risk == "Moderate":
        return (
            "You are in a moderate range. Improve sleep consistency, move more, "
            "and reduce excess alcohol or smoking exposure."
        )

    return (
        "Your health score is low. Focus on better sleep, regular exercise, "
        "balanced nutrition, and reducing risky habits."
    )


def predict_from_form(
    email,
    age,
    bmi,
    exercise_frequency,
    diet_quality,
    sleep_hours,
    smoking_status,
    alcohol_consumption,
):
    try:
        payload = {
            "email": email,
            "age": float(age),
            "bmi": float(bmi),
            "exercise_frequency": float(exercise_frequency),
            "diet_quality": float(diet_quality),
            "sleep_hours": float(sleep_hours),
            "smoking_status": float(smoking_status),
            "alcohol_consumption": float(alcohol_consumption),
        }

        feature_row = pd.DataFrame(
            [
                {
                    "Age": payload["age"],
                    "BMI": payload["bmi"],
                    "Exercise_Frequency": payload["exercise_frequency"],
                    "Diet_Quality": payload["diet_quality"],
                    "Sleep_Hours": payload["sleep_hours"],
                    "Smoking_Status": payload["smoking_status"],
                    "Alcohol_Consumption": payload["alcohol_consumption"],
                }
            ]
        )

        score = float(MODEL.predict(feature_row)[0])
        score = max(0.0, min(100.0, score))
        risk = classify_risk(score)
        recommendation = build_recommendations(score)

        save_prediction_record(str(email), payload, score, risk)

        return f"{score:.2f}", f"Risk: {risk}\n\n{recommendation}"

    except (KeyError, TypeError, ValueError, RuntimeError, OSError) as exc:  # pragma: no cover - UI guard
        return "Error", f"Prediction failed: {exc}"


# ============================================================
# 🌿 NUTRIWELL - FRESH GREEN INTERFACE
# ============================================================

CUSTOM_CSS = """
body {
    background: #F4FBF6 !important;
}

.gradio-container {
    max-width: 1050px !important;
    margin: auto !important;
    background: #F4FBF6 !important;
    font-family: Arial, sans-serif !important;
}

/* Header */
.nutri-header {
    background: linear-gradient(135deg, #2E7D32, #43A047);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(46, 125, 50, 0.20);
}

.nutri-header h1 {
    font-size: 38px !important;
    margin-bottom: 8px !important;
}

.nutri-header p {
    font-size: 16px !important;
    margin: 5px 0 !important;
}

/* Section cards */
.section-card {
    background: white !important;
    border: 1px solid #C8E6C9 !important;
    border-radius: 18px !important;
    padding: 20px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.08);
}

/* Section headings */
.section-title {
    color: #2E7D32;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 12px;
}

/* Labels */
label span {
    color: #1B4332 !important;
    font-weight: 600 !important;
}

/* Input boxes */
input,
textarea {
    border: 1px solid #A5D6A7 !important;
    border-radius: 10px !important;
}

input:focus,
textarea:focus {
    border-color: #43A047 !important;
    box-shadow: 0 0 0 2px rgba(67, 160, 71, 0.15) !important;
}

/* Predict button */
.primary-btn {
    background: #43A047 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    padding: 14px !important;
    margin: 10px 0 22px 0 !important;
}

.primary-btn:hover {
    background: #2E7D32 !important;
}

/* Result area */
.result-box {
    background: #E8F5E9 !important;
    border: 2px solid #A5D6A7 !important;
    border-radius: 18px !important;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #558B5A;
    font-size: 14px;
    padding: 15px;
}
"""


with gr.Blocks(
    title="NutriWell - Health & Wellness",
    css=CUSTOM_CSS,
) as demo:

    # Header
    gr.HTML(
        """
        <div class="nutri-header">
            <h1>🥗 NutriWell</h1>
            <p>Your Personal Health & Wellness Assistant</p>
            <p>
                Enter your health and lifestyle information to receive
                a personalized health assessment.
            </p>
        </div>
        """
    )

    # Personal information
    with gr.Group(elem_classes="section-card"):

        gr.HTML(
            '<div class="section-title">👤 Personal Information</div>'
        )

        with gr.Row():
            email = gr.Textbox(
                label="📧 Email",
                placeholder="Enter your email address",
            )

            age = gr.Number(
                label="🎂 Age",
                precision=0,
                minimum=1,
                maximum=120,
            )

            bmi = gr.Number(
                label="⚖️ BMI",
                precision=2,
            )

    # Lifestyle information
    with gr.Group(elem_classes="section-card"):

        gr.HTML(
            '<div class="section-title">🌿 Lifestyle Information</div>'
        )

        with gr.Row():
            exercise_frequency = gr.Number(
                label="🏃 Exercise Frequency (days/week)",
                precision=0,
            )

            diet_quality = gr.Number(
                label="🥗 Diet Quality (0-100)",
                precision=2,
            )

            sleep_hours = gr.Number(
                label="😴 Sleep Hours",
                precision=2,
            )

    # Health habits
    with gr.Group(elem_classes="section-card"):

        gr.HTML(
            '<div class="section-title">❤️ Health Habits</div>'
        )

        with gr.Row():
            smoking_status = gr.Number(
                label="🚭 Smoking Status (0/1)",
                precision=0,
            )

            alcohol_consumption = gr.Number(
                label="🍷 Alcohol Consumption",
                precision=2,
            )

    # Prediction button
    predict_btn = gr.Button(
        "🔍 Check My Health",
        elem_classes="primary-btn",
        variant="primary",
        size="lg",
    )

    # Results
    with gr.Group(elem_classes="section-card"):

        gr.HTML(
            '<div class="section-title">❤️ Your Wellness Result</div>'
        )

        with gr.Row():
            prediction = gr.Textbox(
                label="📊 Health Score",
                placeholder="Your health score will appear here",
                interactive=False,
            )

            recommendations = gr.Textbox(
                label="💡 Personalized Recommendation",
                placeholder="Your recommendation will appear here",
                lines=5,
                interactive=False,
            )

    # Footer
    gr.HTML(
        """
        <div class="footer-text">
            🌱 NutriWell — Small healthy choices create a healthier life.
        </div>
        """
    )

    # Existing prediction connection - unchanged
    predict_btn.click(
        predict_from_form,
        inputs=[
            email,
            age,
            bmi,
            exercise_frequency,
            diet_quality,
            sleep_hours,
            smoking_status,
            alcohol_consumption,
        ],
        outputs=[
            prediction,
            recommendations,
        ],
    )


if __name__ == "__main__":
    demo.launch()