import joblib
import pandas as pd

# Load trained model
model = joblib.load("../models/model_predict.pkl")


def predict_health_risk(
    age,
    bmi,
    exercise_frequency,
    diet_quality,
    sleep_hours,
    smoking_status,
    alcohol_consumption
):

    data = pd.DataFrame([{
        "Age": age,
        "BMI": bmi,
        "Exercise_Frequency": exercise_frequency,
        "Diet_Quality": diet_quality,
        "Sleep_Hours": sleep_hours,
        "Smoking_Status": smoking_status,
        "Alcohol_Consumption": alcohol_consumption
    }])

    # Predict health score
    health_score = model.predict(data)[0]

    # Keep score between 0 and 100
    health_score = max(0, min(100, health_score))

    # Determine risk level
    if health_score >= 70:
        risk_level = "Low"
    elif health_score >= 40:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return health_score, risk_level


# Example
score, risk = predict_health_risk(
    age=25,
    bmi=22,
    exercise_frequency=5,
    diet_quality=80,
    sleep_hours=8,
    smoking_status=0,
    alcohol_consumption=1
)

print(f"Health Score: {score:.2f}")
print(f"Health Risk Level: {risk}")