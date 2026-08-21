import os

import joblib
from preprocess import preprocess_data
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from xgboost import XGBRegressor

# -----------------------------
# 1. Load and preprocess data
# -----------------------------

data_path = "dataset/synthetic_health_data.csv"

X, y = preprocess_data(data_path)

print("Data loaded successfully!")
print("Features:", X.shape)
print("Target:", y.shape)


# -----------------------------
# 2. Train-test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 3. Create XGBoost model
# -----------------------------

model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

# -----------------------------
# 4. 5-Fold Cross Validation
# -----------------------------

kfold = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=kfold,
    scoring="r2"
)

print("\n========== 5-FOLD CROSS VALIDATION ==========")

for i, score in enumerate(cv_scores, start=1):
    print(f"Fold {i} R²: {score:.4f}")

print(f"Mean R²: {cv_scores.mean():.4f}")
print(f"Std R² : {cv_scores.std():.4f}")


# -----------------------------
# 4. Train model
# -----------------------------

print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

# -----------------------------
# Feature Importance
# -----------------------------

print("\n========== FEATURE IMPORTANCE ==========")

feature_importance = model.feature_importances_

importance_df = (
    __import__("pandas")
    .DataFrame({
        "Feature": X.columns,
        "Importance": feature_importance
    })
    .sort_values(by="Importance", ascending=False)
)

print(importance_df.to_string(index=False))

print("Training completed!")


# -----------------------------
# 5. Make predictions
# -----------------------------

y_pred = model.predict(X_test)


# -----------------------------
# 6. Evaluate model
# -----------------------------

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)


print("\n========== MODEL EVALUATION ==========")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# -----------------------------
# 7. Save model
# -----------------------------

os.makedirs("../models", exist_ok=True)

model_path = "../models/model_predict.pkl"

joblib.dump(model, model_path)

print(f"\nModel saved successfully at: {model_path}")