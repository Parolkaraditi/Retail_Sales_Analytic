
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "results" / "eda"
OUTPUT_DIR = BASE_DIR / "results" / "advanced"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load analytical dataset
sales = pd.read_csv(DATA_DIR / "sales_analysis.csv")
sales["order_date"] = pd.to_datetime(sales["order_date"])

# 1. Top 5 customers
top_customers = (
    sales.groupby("customer_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTOP 5 CUSTOMERS")
print(top_customers)

# 2. Top 5 products
top_products = (
    sales.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTOP 5 PRODUCTS")
print(top_products)

# 3. Monthly revenue growth
monthly = (
    sales.groupby(sales["order_date"].dt.to_period("M"))["revenue"]
    .sum()
    .sort_index()
)

monthly_growth = monthly.pct_change() * 100

print("\nMONTHLY REVENUE GROWTH (%)")
print(monthly_growth.round(2))

# 4. Repeat vs one-time customers
customer_orders = sales.groupby("customer_id")["order_id"].nunique()

repeat_customers = (customer_orders > 1).sum()
one_time_customers = (customer_orders == 1).sum()

print("\nCUSTOMER SEGMENTATION")
print("Repeat Customers:", repeat_customers)
print("One-time Customers:", one_time_customers)

# 5. Category contribution
category_revenue = sales.groupby("category")["revenue"].sum()

category_contribution = (
    category_revenue / category_revenue.sum()
) * 100

print("\nCATEGORY CONTRIBUTION (%)")
print(category_contribution.round(2))

# 6. Highest revenue city
city_revenue = sales.groupby("city")["revenue"].sum()

print("\nHIGHEST REVENUE CITY")
print(city_revenue.idxmax(), "-", city_revenue.max())

# 7. Average quantity per order
order_quantity = sales.groupby("order_id")["quantity"].sum()

print("\nAVERAGE QUANTITY PER ORDER")
print(round(order_quantity.mean(), 2))

# Save reports
top_customers.to_csv(OUTPUT_DIR / "top_customers.csv")
top_products.to_csv(OUTPUT_DIR / "top_products.csv")
monthly_growth.to_csv(OUTPUT_DIR / "monthly_growth.csv")
category_contribution.to_csv(
    OUTPUT_DIR / "category_contribution.csv"
)

print("\nAdvanced business analysis completed!")
print("Results saved in:", OUTPUT_DIR)
