import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (.env is one level up)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Database connection parameters
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

# Build the database URL
db_url = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create a SQLAlchemy engine
engine = create_engine(db_url)

# Load the CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'fraud_oracle.csv')
df = pd.read_csv(csv_file_path)

print(f"✅ CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns.")

# Insert data into the database
try:
    df.to_sql('model_data_w_dummy', con=engine, if_exists='append', index=False)
    print("✅ Data inserted successfully into 'model_data_w_dummy' table.")

except Exception as e:
    print("❌ Failed to insert data.")
    print(e)
