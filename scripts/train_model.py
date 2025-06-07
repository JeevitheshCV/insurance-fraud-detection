import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Paths
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_data.csv'))
model_save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl'))

# Ensure models directory exists
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# Load Preprocessed Data
df = pd.read_csv(data_path)
print(f"✅ Loaded preprocessed data: {df.shape[0]} rows, {df.shape[1]} columns.")

# Split into Features and Target
X = df.drop('FraudFound_P', axis=1)
y = df['FraudFound_P']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"✅ Train size: {X_train.shape[0]} rows | Test size: {X_test.shape[0]} rows")

# Model - Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # Handling imbalanced data
)

# Train the model
model.fit(X_train, y_train)
print(f"✅ Model trained successfully.")

# Save the model
joblib.dump(model, model_save_path)
print(f"✅ Model saved to {model_save_path}")

# Evaluate Model
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print("\n📊 Evaluation Metrics:")
print(f"Accuracy     : {accuracy:.4f}")
print(f"Precision    : {precision:.4f}")
print(f"Recall       : {recall:.4f}")
print(f"F1 Score     : {f1:.4f}")
print(f"ROC-AUC Score: {roc_auc:.4f}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

print("\n🧩 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
