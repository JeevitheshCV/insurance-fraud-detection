# scripts/make_monitoring_ui_artifacts.py

import os
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from sklearn.metrics import roc_curve, auc, precision_recall_curve

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
REFERENCE_DATA_PATH = os.path.join(BASE_DIR, "data", "reference_data.csv")
MONITORING_DATA_PATH = os.path.join(BASE_DIR, "data", "monitoring_data.csv")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "monitoring_artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

DASHBOARD_DRIFT_PATH = os.path.join(ARTIFACTS_DIR, "drift_report.html")
DASHBOARD_PERFORMANCE_PATH = os.path.join(ARTIFACTS_DIR, "performance_report.html")
ROC_CURVE_PATH = os.path.join(ARTIFACTS_DIR, "roc_curve.png")
PR_CURVE_PATH = os.path.join(ARTIFACTS_DIR, "pr_curve.png")
SHAP_BEESWARM_PATH = os.path.join(ARTIFACTS_DIR, "beeswarm.png")
SHAP_FEATURE_IMPORTANCE_PATH = os.path.join(ARTIFACTS_DIR, "feature_importance.png")

def main():
    # ─── Load model & data ────────────────────────────────────────────────────────
    print(f"✅ Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)

    print(f"✅ Loading monitoring data from {MONITORING_DATA_PATH}...")
    df = pd.read_csv(MONITORING_DATA_PATH)
    print(f"Monitoring Data Columns: {df.columns.tolist()}")

    # split out truth & preds
    y_true = df["actual"].values
    y_pred = df["prediction"].values
    feature_cols = [c for c in df.columns if c not in ["actual", "prediction"]]
    X_monitor = df[feature_cols]

    print(f"✅ Loading reference data from {REFERENCE_DATA_PATH}...")
    reference_data = pd.read_csv(REFERENCE_DATA_PATH)
    print(f"Reference Data Columns: {reference_data.columns.tolist()}")

    # ─── Common features + filter out constants ─────────────────────────────────
    common_features = list(set(reference_data.columns) & set(X_monitor.columns))
    print(f"✅ Common Features ({len(common_features)}): {common_features}")

    varying_features = [
        f for f in common_features
        if reference_data[f].nunique() > 1 and X_monitor[f].nunique() > 1
    ]
    if not varying_features:
        print("⚠️ No features with enough variation for drift analysis; skipping drift report.")
    else:
        print(f"✅ Using {len(varying_features)} varying features for drift: {varying_features}")

    # ─── Drift Report ──────────────────────────────────────────────────────────
    if varying_features:
        try:
            drift_mapping = ColumnMapping(
                numerical_features=varying_features,
                categorical_features=[],
                target=None,
                prediction=None,
            )
            drift_report = Report(metrics=[DataDriftPreset()])
            drift_report.run(
                reference_data=reference_data[varying_features],
                current_data=X_monitor[varying_features],
                column_mapping=drift_mapping
            )
            drift_report.save_html(DASHBOARD_DRIFT_PATH)
            print(f"✅ Drift report saved to {DASHBOARD_DRIFT_PATH}")
        except ZeroDivisionError:
            print("⚠️ Evidently computed zero drift metrics—skipping drift dashboard.")

    # ─── Performance Report ────────────────────────────────────────────────────
    print("✅ Generating Performance Report...")
    perf_df = pd.DataFrame({"target": y_true, "prediction": y_pred})
    perf_mapping = ColumnMapping(
        numerical_features=[],
        categorical_features=[],
        target="target",
        prediction="prediction",
    )
    perf_report = Report(metrics=[ClassificationPreset()])
    perf_report.run(
        reference_data=perf_df,
        current_data=perf_df,
        column_mapping=perf_mapping
    )
    perf_report.save_html(DASHBOARD_PERFORMANCE_PATH)
    print(f"✅ Performance report saved to {DASHBOARD_PERFORMANCE_PATH}")

    # ─── ROC Curve ─────────────────────────────────────────────────────────────
    print("✅ Generating ROC Curve...")
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, lw=2, label=f"ROC AUC = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.grid()
    plt.savefig(ROC_CURVE_PATH)
    plt.close()
    print(f"✅ ROC curve saved to {ROC_CURVE_PATH}")

    # ─── Precision-Recall Curve ───────────────────────────────────────────────
    print("✅ Generating Precision-Recall Curve...")
    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    plt.figure()
    plt.plot(recall, precision, lw=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.grid()
    plt.savefig(PR_CURVE_PATH)
    plt.close()
    print(f"✅ PR curve saved to {PR_CURVE_PATH}")

    # ─── SHAP Summary Plots ────────────────────────────────────────────────────
    print("✅ Generating SHAP Summary Plots...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_monitor)

    # Beeswarm
    plt.figure()
    shap.summary_plot(shap_values, X_monitor, show=False)
    plt.tight_layout()
    plt.savefig(SHAP_BEESWARM_PATH, bbox_inches="tight")
    plt.close()
    print(f"✅ SHAP beeswarm plot saved to {SHAP_BEESWARM_PATH}")

    # Feature importance bar
    plt.figure()
    shap.summary_plot(shap_values, X_monitor, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(SHAP_FEATURE_IMPORTANCE_PATH, bbox_inches="tight")
    plt.close()
    print(f"✅ SHAP feature importance plot saved to {SHAP_FEATURE_IMPORTANCE_PATH}")

if __name__ == "__main__":
    main()
