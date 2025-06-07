# import os
# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv

# # Load environment variables
# env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(dotenv_path=env_path)

# # DB Config
# db_host = os.getenv('db_host')
# db_port = os.getenv('db_port')
# db_name = os.getenv('db_name')
# db_username = os.getenv('db_username')
# db_password = os.getenv('db_password')

# # Build DB URL
# db_url = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# # SQLAlchemy engine
# engine = create_engine(db_url)

# # ✅ Correct full path to the preprocessed CSV
# csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_data.csv')
# csv_file_path = os.path.abspath(csv_file_path)

# # Load Preprocessed CSV
# df = pd.read_csv(csv_file_path)

# print(f"Loaded preprocessed CSV: {df.shape[0]} rows, {df.shape[1]} columns.")

# # Insert data into DB
# try:
#     df.to_sql('model_data_w_dummy', con=engine, if_exists='append', index=False)
#     print(f"Data inserted into `model_data_w_dummy` table successfully.")

# except Exception as e:
#     print("Failed to insert data into DB.")
#     print(e)


import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# DB Config
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

# Database URL
db_url = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create engine
engine = create_engine(db_url)

# Path to CSV
csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'fraud_oracle.csv'))

# Load the raw CSV
df = pd.read_csv(csv_file_path)
print(f"✅ Loaded raw CSV: {df.shape[0]} rows, {df.shape[1]} columns.")

# --------------------------------
# Feature Engineering
# --------------------------------

# Select meaningful features
meaningful_features = [
    'NumberOfSuppliments', 'AgeOfVehicle', 'AgeOfPolicyHolder', 'Month',
    'Deductible', 'MonthClaimed', 'Make', 'AddressChange_Claim',
    'PastNumberOfClaims', 'VehiclePrice', 'VehicleCategory', 'Fault'
]

df_meaningful = df[meaningful_features].copy()

# Manual Grouping (feature engineering)
df_meaningful['NumberOfSuppliments'] = df_meaningful['NumberOfSuppliments'].replace({
    'none': 'none or 1 to 2',
    '1 to 2': 'none or 1 to 2',
    '3 to 5': 'more than 3',
    'more than 5': 'more than 3'
})
df_meaningful['AgeOfVehicle'] = df_meaningful['AgeOfVehicle'].replace({
    '3 years': '3-4 years',
    '4 years': '3-4 years',
    '5 years': 'more than 5 years',
    '6 years': 'more than 5 years',
    '7 years': 'more than 5 years',
    'more than 7': 'more than 5 years'
})
df_meaningful['AgeOfPolicyHolder'] = df_meaningful['AgeOfPolicyHolder'].replace({
    '41 to 50': '41 to 65',
    '51 to 65': '41 to 65'
})
df_meaningful['Month'] = df_meaningful['Month'].replace({
    'Jan': 'Jan-Feb',
    'Feb': 'Jan-Feb'
})
df_meaningful['Deductible'] = df_meaningful['Deductible'].astype(str)
df_meaningful['MonthClaimed'] = df_meaningful['MonthClaimed'].replace({
    'Jan': 'Jan-Feb',
    'Feb': 'Jan-Feb'
})
df_meaningful['Make'] = df_meaningful['Make'].replace({
    'Lexus': 'Lexus/Ferrari/Porche/Jaguar',
    'Ferrari': 'Lexus/Ferrari/Porche/Jaguar',
    'Porche': 'Lexus/Ferrari/Porche/Jaguar',
    'Jaguar': 'Lexus/Ferrari/Porche/Jaguar'
})
df_meaningful['VehiclePrice'] = df_meaningful['VehiclePrice'].replace({
    '20000 to 29000': '20000 to 39000',
    '30000 to 39000': '20000 to 39000'
})

# Add Target Variable
df_meaningful['FraudFound_P'] = df['FraudFound_P']

# --------------------------------
# Dummy Encoding
# --------------------------------
df_X = df_meaningful.drop('FraudFound_P', axis=1)
model_data_w_dummy = pd.get_dummies(df_X, drop_first=True)
model_data_w_dummy['FraudFound_P'] = df_meaningful['FraudFound_P']

print(f"Preprocessed DataFrame shape: {model_data_w_dummy.shape}")

# --------------------------------
# Save Locally as CSV
# --------------------------------
preprocessed_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_data.csv'))
model_data_w_dummy.to_csv(preprocessed_csv_path, index=False)
print(f"Preprocessed CSV saved at: {preprocessed_csv_path}")

# --------------------------------
# Insert into RDS
# --------------------------------
try:
    model_data_w_dummy.to_sql('model_data_w_dummy', con=engine, if_exists='replace', index=False)
    print(f"Data inserted into `model_data_w_dummy` table successfully.")
except Exception as e:
    print("Failed to insert data into DB.")
    print(e)
