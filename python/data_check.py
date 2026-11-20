
from pathlib import Path
import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# MySQL connection
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Existing database tables
tables = ["orders", "customers", "products", "orders_details"]

try:
    for table in tables:
        print("\n" + "=" * 60)
        print(f"TABLE: {table.upper()}")
        print("=" * 60)

        query = f"SELECT * FROM `{table}`"
        df = pd.read_sql(query, connection)

        print("\nShape:", df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

        print("\nFirst 5 Records:")
        print(df.head())

finally:
    connection.close()
    print("\nMySQL connection closed.")
