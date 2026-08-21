import json
from datetime import datetime
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
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
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
        return "Maintain your current health habits. Keep exercising regularly and eating a balanced diet."
    if risk == "Moderate":
        return "You are in a moderate range. Improve sleep consistency, move more, and reduce excess alcohol or smoking exposure."
    return "Your health score is low. Focus on better sleep, regular exercise, balanced nutrition, and reducing risky habits."


def predict_from_form(email, age, bmi, exercise_frequency, diet_quality, sleep_hours, smoking_status, alcohol_consumption):
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

        feature_row = pd.DataFrame([
            {
                "Age": payload["age"],
                "BMI": payload["bmi"],
                "Exercise_Frequency": payload["exercise_frequency"],
                "Diet_Quality": payload["diet_quality"],
                "Sleep_Hours": payload["sleep_hours"],
                "Smoking_Status": payload["smoking_status"],
                "Alcohol_Consumption": payload["alcohol_consumption"],
            }
        ])

        score = float(MODEL.predict(feature_row)[0])
        score = max(0.0, min(100.0, score))
        risk = classify_risk(score)
        recommendation = build_recommendations(score)

        save_prediction_record(str(email), payload, score, risk)

        return f"{score:.2f}", f"Risk: {risk}\n\n{recommendation}"
    except Exception as exc:  # pragma: no cover - UI guard
        return "Error", f"Prediction failed: {exc}"


with gr.Blocks(title="NutriWell") as demo:
    gr.Markdown("# NutriWell Health Prediction")

    with gr.Row():
        email = gr.Textbox(label="Email")
        age = gr.Number(label="Age", precision=0)
        bmi = gr.Number(label="BMI", precision=2)

    with gr.Row():
        exercise_frequency = gr.Number(label="Exercise frequency (days/week)", precision=0)
        diet_quality = gr.Number(label="Diet quality (0-100)", precision=2)
        sleep_hours = gr.Number(label="Sleep hours", precision=2)

    with gr.Row():
        smoking_status = gr.Number(label="Smoking status (0/1)", precision=0)
        alcohol_consumption = gr.Number(label="Alcohol consumption", precision=2)

    predict_btn = gr.Button("Predict")
    prediction = gr.Textbox(label="Health Score")
    recommendations = gr.Textbox(label="Recommendations", lines=5)

    predict_btn.click(
        predict_from_form,
        inputs=[email, age, bmi, exercise_frequency, diet_quality, sleep_hours, smoking_status, alcohol_consumption],
        outputs=[prediction, recommendations],
    )

if __name__ == "__main__":
    demo.launch()
