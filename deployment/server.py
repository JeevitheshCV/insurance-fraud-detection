import os
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import shap

# ——— Resolve the absolute path to your trained model ———
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

# Load the model
model = joblib.load(MODEL_PATH)

# Initialize SHAP explainer for a tree-based model
explainer = shap.TreeExplainer(model)

# ——— FastAPI app and schemas ———
app = FastAPI()

class PredictionRequest(BaseModel):
    features: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to the Insurance Fraud Detection API"}

@app.post("/predict")
def predict(request: PredictionRequest):
    input_df = pd.DataFrame([request.features])
    pred = int(model.predict(input_df)[0])
    return {"prediction": pred}

@app.post("/explain")
def explain(request: PredictionRequest):
    input_df = pd.DataFrame([request.features])
    pred = int(model.predict(input_df)[0])

    # Compute SHAP values
    shap_vals_all = explainer.shap_values(input_df)
    shap_vals = shap_vals_all[pred][0]

    contribs = dict(zip(input_df.columns, shap_vals))
    top10 = sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
    top10_formatted = [{"feature": f, "shap_value": float(v)} for f, v in top10]

    return {
        "prediction": pred,
        "top_shap_values": top10_formatted
    }
