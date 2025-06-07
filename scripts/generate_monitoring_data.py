# # scripts/generate_monitoring_data.py

# import os
# import pandas as pd
# import joblib
# from sklearn.model_selection import train_test_split

# # Paths

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
# DATA_PATH = os.path.join(BASE_DIR, "data", "preprocessed_data.csv")
# MONITORING_DATA_PATH = os.path.join(BASE_DIR, "data", "monitoring_data.csv")


# def main():
#     print("✅ Loading model...")
#     print(MODEL_PATH)
#     model = joblib.load(MODEL_PATH)

#     print("✅ Loading preprocessed data...")
#     df = pd.read_csv(DATA_PATH)

#     # Target column
#     target_col = "FraudFound_P"

#     # Feature columns
#     X = df.drop(columns=[target_col])
#     y = df[target_col]

#     # Train-test split (same random_state as before)
#     print("✅ Splitting data...")
#     _, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#     print("✅ Making predictions...")
#     y_pred = model.predict(X_test)

#     print("✅ Preparing monitoring data...")
#     monitoring_df = pd.DataFrame({
#         "actual": y_test.values,
#         "prediction": y_pred
#     })

#     print(f"✅ Saving monitoring data to {MONITORING_DATA_PATH}")
#     monitoring_df.to_csv(MONITORING_DATA_PATH, index=False)
#     print(f"✅ Monitoring data generated: {monitoring_df.shape[0]} rows.")

# if __name__ == "__main__":
#     main()


# Update to scripts/generate_monitoring_data.py

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "preprocessed_data.csv")
MONITORING_DATA_PATH = os.path.join(BASE_DIR, "data", "monitoring_data.csv")
REFERENCE_DATA_PATH = os.path.join(BASE_DIR, "data", "reference_data.csv")

def main():
    print("✅ Loading model...")
    model = joblib.load(MODEL_PATH)

    print("✅ Loading preprocessed data...")
    df = pd.read_csv(DATA_PATH)

    # Target column
    target_col = "FraudFound_P"
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Train-test split
    print("✅ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print("✅ Making predictions...")
    y_pred = model.predict(X_test)

    print("✅ Preparing monitoring data...")
    monitoring_df = X_test.copy()
    monitoring_df["actual"] = y_test.values
    monitoring_df["prediction"] = y_pred
    monitoring_df.to_csv(MONITORING_DATA_PATH, index=False)

    print("✅ Preparing reference data...")
    reference_df = X_train.copy()
    reference_df.to_csv(REFERENCE_DATA_PATH, index=False)

    print(f"✅ Monitoring data generated: {monitoring_df.shape[0]} rows.")
    print(f"✅ Reference data generated: {reference_df.shape[0]} rows.")

if __name__ == "__main__":
    main()
