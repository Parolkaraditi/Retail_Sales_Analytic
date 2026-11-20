from pathlib import Path
import os
import mysql.connector
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

print("Project folder:", BASE_DIR)
print("ENV file exists:", (BASE_DIR / ".env").exists())
print("Password loaded:", bool(os.getenv("DB_PASSWORD")))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "retail_sales")

if not DB_PASSWORD:
    raise ValueError(
        "MySQL password missing. Please check your .env file."
    )

connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

if connection.is_connected():
    print("MySQL connection successful!")

connection.close()