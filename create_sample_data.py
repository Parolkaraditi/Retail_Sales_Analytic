import pandas as pd
from pathlib import Path

DATA_DIR = Path("dataset")
DATA_DIR.mkdir(exist_ok=True)

customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104, 105, 106],
    "customer_name": ["Aarav Sharma", "Priya Patel", "Rahul Verma",
                      "Sneha Joshi", "Rohan Mehta", "Ananya Singh"],
    "city": ["Mumbai", "Pune", "Indore", "Bhopal", "Delhi", "Nashik"],
    "gender": ["Male", "Female", "Male", "Female", "Male", "Female"]
})

orders = pd.DataFrame({
    "order_id": [1001, 1002, 1003, 1004, 1005, 1006],
    "customer_id": [101, 102, 103, 104, 105, 106],
    "order_date": ["2026-01-05", "2026-01-08", "2026-02-10",
                   "2026-02-15", "2026-03-01", "2026-03-05"]
})

products = pd.DataFrame({
    "product_id": [201, 202, 203, 204, 205],
    "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
    "category": ["Electronics", "Accessories", "Accessories",
                 "Electronics", "Accessories"]
})

orders_details = pd.DataFrame({
    "order_id": [1001, 1001, 1002, 1003, 1004, 1005, 1006],
    "product_id": [201, 202, 203, 204, 205, 201, 202],
    "quantity": [1, 2, 1, 1, 2, 1, 3],
    "unit_price": [55000, 500, 1200, 18000, 2000, 55000, 500]
})

customers.to_csv(DATA_DIR / "customers.csv", index=False)
orders.to_csv(DATA_DIR / "orders.csv", index=False)
products.to_csv(DATA_DIR / "products.csv", index=False)
orders_details.to_csv(DATA_DIR / "orders_details.csv", index=False)

print("All four CSV files created successfully!")

for file in DATA_DIR.glob("*.csv"):
    print(file)
