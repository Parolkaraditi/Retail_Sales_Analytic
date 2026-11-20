
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "results" / "eda"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# Load cleaned datasets
# Load cleaned datasets
orders = pd.read_csv(
    DATA_DIR / "orders_cleaned.csv",
    parse_dates=["order_date"]
)

customers = pd.read_csv(DATA_DIR / "customers_cleaned.csv")
products = pd.read_csv(DATA_DIR / "products_cleaned.csv")
details = pd.read_csv(DATA_DIR / "orders_details_cleaned.csv")

sales = (
    details
    .merge(orders, on="order_id", how="inner")
    .merge(customers, on="customer_id", how="inner")
    .merge(products, on="product_id", how="inner")
)

# Calculate revenue
sales["revenue"] = sales["quantity"] * sales["unit_price"]

# Overall business metrics
total_revenue = sales["revenue"].sum()
total_orders = orders["order_id"].nunique()
total_customers = customers["customer_id"].nunique()
total_products = products["product_id"].nunique()
average_order_value = sales.groupby("order_id")["revenue"].sum().mean()

print("\n========== BUSINESS OVERVIEW ==========")
print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Total Products:", total_products)
print("Average Order Value:", round(average_order_value, 2))

# Monthly revenue
monthly = (
    sales.groupby(sales["order_date"].dt.to_period("M"))["revenue"]
    .sum()
)

print("\nMonthly Revenue:")
print(monthly)

plt.figure(figsize=(9, 5))
monthly.index = monthly.index.astype(str)
monthly.plot(kind="bar")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue.png")
plt.close()

# Category revenue
category = sales.groupby("category")["revenue"].sum().sort_values(ascending=False)

print("\nCategory Revenue:")
print(category)

plt.figure(figsize=(8, 5))
category.plot(kind="bar")
plt.title("Category-wise Revenue")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_revenue.png")
plt.close()

# Top products
top_products = (
    sales.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProduct Revenue:")
print(top_products)

plt.figure(figsize=(9, 5))
top_products.plot(kind="bar")
plt.title("Product-wise Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "product_revenue.png")
plt.close()

# City revenue
city_revenue = sales.groupby("city")["revenue"].sum().sort_values(ascending=False)

print("\nCity-wise Revenue:")
print(city_revenue)

plt.figure(figsize=(9, 5))
city_revenue.plot(kind="bar")
plt.title("City-wise Revenue")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "city_revenue.png")
plt.close()

# Customer revenue
customer_revenue = (
    sales.groupby("customer_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCustomer-wise Revenue:")
print(customer_revenue)

plt.figure(figsize=(9, 5))
customer_revenue.plot(kind="bar")
plt.title("Customer-wise Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "customer_revenue.png")
plt.close()

# Save merged analytical dataset
sales.to_csv(OUTPUT_DIR / "sales_analysis.csv", index=False)

print("\nEDA completed successfully!")
print("Charts and analysis saved in:", OUTPUT_DIR)
