
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "dataset" / "cleaned"
EXCEL_DIR = BASE_DIR / "excel"

EXCEL_DIR.mkdir(parents=True, exist_ok=True)

customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
details = pd.read_csv(DATA_DIR / "orders_details.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

# Validate required columns
required = {
    "customers": {"customer_id", "customer_name"},
    "orders": {"order_id", "customer_id", "order_date"},
    "details": {"order_id", "product_id", "quantity", "unit_price"},
    "products": {"product_id", "product_name", "category"}
}

datasets = {
    "customers": customers,
    "orders": orders,
    "details": details,
    "products": products
}

for name, cols in required.items():
    missing = cols - set(datasets[name].columns)
    if missing:
        raise ValueError(
            f"{name} is missing columns: {missing}. "
            f"Available columns: {datasets[name].columns.tolist()}"
        )

# Convert dates
orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

# Merge datasets
df = details.merge(
    orders,
    on="order_id",
    how="left",
    validate="many_to_one"
)

df = df.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

df = df.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# Calculate sales
if "discount" in df.columns:
    discount = pd.to_numeric(
        df["discount"], errors="coerce"
    ).fillna(0)

    df["discount"] = discount

    df["sales"] = (
        df["quantity"] * df["unit_price"] *
        (1 - df["discount"])
    )
else:
    df["sales"] = df["quantity"] * df["unit_price"]

# Calculate year and month
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%B")

# Overall KPIs
total_sales = df["sales"].sum()
total_orders = orders["order_id"].nunique()
total_customers = customers["customer_id"].nunique()
total_quantity = df["quantity"].sum()
average_order_value = (
    total_sales / total_orders if total_orders else 0
)

kpis = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Orders",
        "Total Customers",
        "Total Quantity Sold",
        "Average Order Value"
    ],
    "Value": [
        total_sales,
        total_orders,
        total_customers,
        total_quantity,
        average_order_value
    ]
})

# Category analysis
category_analysis = df.groupby(
    "category", dropna=False
).agg(
    total_sales=("sales", "sum"),
    total_quantity=("quantity", "sum"),
    total_orders=("order_id", "nunique")
).reset_index()

# Product analysis
product_analysis = df.groupby(
    "product_name", dropna=False
).agg(
    total_sales=("sales", "sum"),
    total_quantity=("quantity", "sum")
).reset_index()

product_analysis = product_analysis.sort_values(
    "total_sales", ascending=False
)

# Customer analysis
customer_analysis = df.groupby(
    "customer_name", dropna=False
).agg(
    total_sales=("sales", "sum"),
    total_orders=("order_id", "nunique")
).reset_index()

customer_analysis = customer_analysis.sort_values(
    "total_sales", ascending=False
)

# Monthly sales
monthly_analysis = df.groupby(
    ["order_year", "order_month"], dropna=False
).agg(
    total_sales=("sales", "sum"),
    total_quantity=("quantity", "sum")
).reset_index()

# Save Excel workbook
output = EXCEL_DIR / "initial_analytics.xlsx"

with pd.ExcelWriter(output, engine="openpyxl") as writer:

    kpis.to_excel(
        writer, sheet_name="KPI Summary", index=False
    )

    category_analysis.to_excel(
        writer, sheet_name="Category Analysis", index=False
    )

    product_analysis.to_excel(
        writer, sheet_name="Product Analysis", index=False
    )

    customer_analysis.to_excel(
        writer, sheet_name="Customer Analysis", index=False
    )

    monthly_analysis.to_excel(
        writer, sheet_name="Monthly Sales", index=False
    )

    df.to_excel(
        writer, sheet_name="Merged Data", index=False
    )

print("\nINITIAL ANALYTICS COMPLETED")
print(kpis)
print("\nExcel report saved:", output)
