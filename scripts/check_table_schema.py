import psycopg2
from dotenv import load_dotenv
import os

# Load env
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_username,
        password=db_password
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'model_data_w_dummy'
        ORDER BY ordinal_position;
    """)
    columns = cur.fetchall()

    print("✅ Table Schema:")
    for col in columns:
        print(f"- {col[0]} ({col[1]})")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error while checking table schema.")
    print(e)
