import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('db_host'),
    port=os.getenv('db_port'),
    database=os.getenv('db_name'),
    user=os.getenv('db_username'),
    password=os.getenv('db_password')
)

cur = conn.cursor()

cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public';""")

tables = cur.fetchall()

print("Tables in the database:")
for table in tables:
    print(table)

cur.close()
conn.close()
