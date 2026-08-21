import pandas as pd


def preprocess_data(file_path):
    # Load dataset
    df = pd.read_csv(file_path)

    # Separate features and target
    X = df.drop(columns=["Health_Score"])
    y = df["Health_Score"]

    # Convert categorical columns into numerical columns
    categorical_columns = X.select_dtypes(include=["object"]).columns

    X = pd.get_dummies(
        X,
        columns=categorical_columns,
        drop_first=True
    )

    return X, y


if __name__ == "__main__":
    X, y = preprocess_data("dataset/synthetic_health_data.csv")

    print("Features:")
    print(X.head())

    print("\nFeature columns:")
    print(X.columns.tolist())

    print("\nTarget:")
    print(y.head())

    print("\nTarget statistics:")
    print(y.describe())