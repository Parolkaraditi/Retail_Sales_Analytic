
from pathlib import Path
import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Connect to MySQL
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

try:
    # Extract tables
    tables = {
        "orders": "SELECT * FROM orders",
        "customers": "SELECT * FROM customers",
        "products": "SELECT * FROM products",
        "orders_details": "SELECT * FROM orders_details"
    }

    data = {}

    for name, query in tables.items():
        data[name] = pd.read_sql(query, connection)

    print("Data extracted successfully!")

finally:
    connection.close()

# Clean text columns
for name, df in data.items():
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Remove exact duplicate rows
    data[name] = df.drop_duplicates().copy()

# Convert order date
data["orders"]["order_date"] = pd.to_datetime(
    data["orders"]["order_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

if data["orders"]["order_date"].isna().any():
    raise ValueError("Invalid or missing order dates found.")

# Convert numeric columns
numeric_columns = {
    "orders": ["order_id", "customer_id"],
    "customers": ["customer_id"],
    "products": ["product_id"],
    "orders_details": [
        "order_id", "product_id", "quantity", "unit_price"
    ]
}

for table, columns in numeric_columns.items():
    for col in columns:
        data[table][col] = pd.to_numeric(
            data[table][col], errors="coerce"
        )

        if data[table][col].isna().any():
            raise ValueError(f"Invalid values in {table}.{col}")

# Validate sales values
details = data["orders_details"]

if (details["quantity"] <= 0).any():
    raise ValueError("Quantity must be greater than zero.")

if (details["unit_price"] < 0).any():
    raise ValueError("Unit price cannot be negative.")

# Validate relationships between tables
orders = data["orders"]
customers = data["customers"]
products = data["products"]

if not orders["customer_id"].isin(customers["customer_id"]).all():
    raise ValueError("Some orders reference unknown customers.")

if not details["order_id"].isin(orders["order_id"]).all():
    raise ValueError("Some order details reference unknown orders.")

if not details["product_id"].isin(products["product_id"]).all():
    raise ValueError("Some order details reference unknown products.")

# Save cleaned datasets
for name, df in data.items():
    output_path = OUTPUT_DIR / f"{name}_cleaned.csv"
    df.to_csv(output_path, index=False)

    print(f"\n{name}:")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Saved:", output_path)

print("\nData cleaning completed successfully!")
