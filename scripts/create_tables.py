import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables (.env is one directory up)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Read DB config
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

# Debugging — print loaded host
print(f"Host: {db_host}")

# Connect to the database
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_username,
        password=db_password
    )
    print("✅ Connection established.")

    # Open and read the SQL file (one level up from scripts/)
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'data_schemas.sql')
    with open(sql_file_path, 'r') as f:
        sql = f.read()

    # Create a cursor and execute
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("✅ Tables created successfully.")

    # Close connection
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error connecting or creating tables.")
    print(e)
