import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read DB config
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

# Connect to the database
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_username,
        password=db_password
    )
    print(f"✅ Connection to {db_host} successful!")
    conn.close()

except Exception as e:
    print("❌ Failed to connect to the database.")
    print(e)
