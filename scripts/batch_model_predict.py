import os
import pandas as pd
import joblib

# Paths
preprocessed_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_data.csv'))
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl'))
batch_predictions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'batch_predictions.csv'))

# Load the model
model = joblib.load(model_path)
print(f"✅ Model loaded successfully from {model_path}")

# Load preprocessed data
df = pd.read_csv(preprocessed_data_path)
print(f"✅ Preprocessed data loaded: {df.shape[0]} rows, {df.shape[1]} columns.")

# Features (drop the target column if exists)
if 'FraudFound_P' in df.columns:
    X = df.drop('FraudFound_P', axis=1)
else:
    X = df

# Make predictions
y_pred = model.predict(X)
y_pred_proba = model.predict_proba(X)[:, 1]  # probability of class 1 (fraud)

# Prepare output DataFrame
predictions_df = X.copy()
predictions_df['Fraud_Predicted'] = y_pred
predictions_df['Fraud_Probability'] = y_pred_proba

# Save predictions
predictions_df.to_csv(batch_predictions_path, index=False)
print(f"✅ Batch predictions saved to {batch_predictions_path}")
