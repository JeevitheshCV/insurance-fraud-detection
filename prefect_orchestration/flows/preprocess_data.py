# from prefect import flow, task
# import pandas as pd
# import psycopg2
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import os

# '''Load raw data from model_data_w_dummy table in RDS.

# Preprocess:
# Drop missing values.
# Dummy encode categorical variables.
# Save preprocessed data locally to data/preprocessed_data.csv.'''

# # Load environment variables
# env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# load_dotenv(dotenv_path=env_path)

# # DB Config
# db_host = os.getenv('db_host')
# db_port = os.getenv('db_port')
# db_name = os.getenv('db_name')
# db_username = os.getenv('db_username')
# db_password = os.getenv('db_password')

# # Build SQLAlchemy engine
# db_url = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# @task
# def load_data_from_db():
#     engine = create_engine(db_url)
#     query = "SELECT * FROM model_data_w_dummy;"
#     df = pd.read_sql(query, con=engine)
#     print(f"✅ Loaded {len(df)} rows from database.")
#     return df

# @task
# def preprocess_data(df):
#     # Example preprocessing: Drop NA, dummy encoding
#     df = df.dropna()
#     df = pd.get_dummies(df, drop_first=True)
#     print(f"✅ Preprocessed data: {df.shape[0]} rows, {df.shape[1]} columns.")
#     return df

# @flow(name="fraud-preprocessing-flow")
# def preprocessing_flow():
#     df_raw = load_data_from_db()
#     df_clean = preprocess_data(df_raw)
    
#     # Save preprocessed data locally (later we upload to S3)
#     output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'preprocessed_data.csv')
#     df_clean.to_csv(output_path, index=False)
#     print(f"✅ Preprocessed data saved at {output_path}")

# if __name__ == "__main__":
#     preprocessing_flow()


from prefect import flow, task
import pandas as pd
import os

# No need for DB connection here

@task
def load_csv():
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'fraud_oracle.csv')
    df = pd.read_csv(csv_file_path)
    print(f"✅ Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

@task
def preprocess_data(df):
    # Example preprocessing: Drop NA, dummy encoding
    df = df.dropna()
    df = pd.get_dummies(df, drop_first=True)
    print(f"✅ Preprocessed data: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

@flow(name="fraud-preprocessing-flow")
def preprocessing_flow():
    df_raw = load_csv()
    df_clean = preprocess_data(df_raw)

    # Save preprocessed data
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'preprocessed_data.csv')
    df_clean.to_csv(output_path, index=False)
    print(f"✅ Preprocessed data saved at {output_path}")

if __name__ == "__main__":
    preprocessing_flow()
