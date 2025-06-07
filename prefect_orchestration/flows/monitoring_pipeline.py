import os
from prefect import flow, task
import subprocess
import boto3
from dotenv import load_dotenv

# Load .env
load_dotenv()

# project root (two levels up from this file)
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# S3 Config
AWS_REGION = "us-east-1"
S3_BUCKET = "insurance-fraud-detection-data"  # your bucket
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "monitoring_artifacts")

@task
def generate_monitoring_data():
    script = os.path.join(PROJECT_ROOT, "scripts", "generate_monitoring_data.py")
    print(f"✅ Generating monitoring data via {script}...")
    # ensure the script runs from the project root
    subprocess.run(["python", script], cwd=PROJECT_ROOT, check=True)

@task
def make_monitoring_artifacts():
    script = os.path.join(PROJECT_ROOT, "scripts", "make_monitoring_ui_artifacts.py")
    print(f"✅ Generating monitoring artifacts via {script}...")
    subprocess.run(["python", script], cwd=PROJECT_ROOT, check=True)

def guess_content_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".png"):
        return "image/png"
    else:
        return "binary/octet-stream"

@task
def upload_artifacts_to_s3():
    print(f"✅ Uploading artifacts from {ARTIFACTS_DIR} to s3://{S3_BUCKET}/monitoring/...")
    s3 = boto3.client("s3", region_name=AWS_REGION)

    for root, _, files in os.walk(ARTIFACTS_DIR):
        for fn in files:
            local_path = os.path.join(root, fn)
            rel_path = os.path.relpath(local_path, ARTIFACTS_DIR).replace("\\", "/")
            s3_key = f"monitoring/{rel_path}"
            s3.upload_file(
                Filename=local_path,
                Bucket=S3_BUCKET,
                Key=s3_key,
                ExtraArgs={"ContentType": guess_content_type(fn)}
            )
            print(f"✅ Uploaded {fn} -> s3://{S3_BUCKET}/{s3_key}")

@flow(name="monitoring_pipeline")
def monitoring_pipeline():
    generate_monitoring_data()
    make_monitoring_artifacts()
    upload_artifacts_to_s3()

if __name__ == "__main__":
    monitoring_pipeline()
