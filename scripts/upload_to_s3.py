import boto3
import os
from dotenv import load_dotenv

# Load environment variables if needed
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# AWS S3 client
s3 = boto3.client('s3')

# Set your bucket name
BUCKET_NAME = 'insurance-fraud-detection-data'  # <-- Replace if your bucket name is different

# Files to upload
local_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl'))
local_predictions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'batch_predictions.csv'))

# S3 paths
s3_model_key = 'models/model.pkl'
s3_predictions_key = 'predictions/batch_predictions.csv'

def upload_file(file_path, bucket_name, s3_key):
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Failed to upload {file_path}")
        print(e)

if __name__ == "__main__":
    upload_file(local_model_path, BUCKET_NAME, s3_model_key)
    upload_file(local_predictions_path, BUCKET_NAME, s3_predictions_key)
