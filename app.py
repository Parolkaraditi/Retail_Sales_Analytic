
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Retail Sales Analytics Dashboard")
st.caption("Analyze sales, customers, products and business performance")

# Dataset paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dataset" / "cleaned"

# Load datasets
@st.cache_data
def load_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    details = pd.read_csv(DATA_DIR / "orders_details.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")

    return customers, orders, details, products

try:
    customers, orders, details, products = load_data()

except Exception as e:
    st.error(f"Unable to load datasets: {e}")
    st.info("Check that all four CSV files exist inside dataset/cleaned/.")
    st.stop()

# Prepare data
orders["order_date"] = pd.to_datetime(orders["order_date"])

details["revenue"] = details["quantity"] * details["unit_price"]

sales = (
    details
    .merge(orders, on="order_id", how="left")
    .merge(products, on="product_id", how="left")
    .merge(customers, on="customer_id", how="left")
)

sales["month"] = sales["order_date"].dt.strftime("%b %Y")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

categories = ["All"] + sorted(
    sales["category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

cities = ["All"] + sorted(
    sales["city"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)

if selected_category != "All":
    sales = sales[sales["category"] == selected_category]

if selected_city != "All":
    sales = sales[sales["city"] == selected_city]

# KPI calculations
total_revenue = sales["revenue"].sum()
total_orders = sales["order_id"].nunique()
total_customers = sales["customer_id"].nunique()
total_products = sales["product_id"].nunique()

# KPI cards
st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Products Sold", f"{total_products:,}")

st.divider()

# Monthly revenue
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    sales.groupby("month", as_index=False)["revenue"]
    .sum()
)

monthly_sales["month_date"] = pd.to_datetime(
    monthly_sales["month"], format="%b %Y"
)

monthly_sales = monthly_sales.sort_values("month_date")

fig_monthly = px.line(
    monthly_sales,
    x="month_date",
    y="revenue",
    markers=True,
    title="Monthly Revenue",
    labels={
        "month_date": "Month",
        "revenue": "Revenue (₹)"
    }
)

st.plotly_chart(fig_monthly, use_container_width=True)

# Category and city analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category-wise Revenue")

    category_sales = (
        sales.groupby("category", as_index=False)["revenue"]
        .sum()
    )

    fig_category = px.pie(
        category_sales,
        names="category",
        values="revenue",
        hole=0.45
    )

    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    st.subheader("City-wise Revenue")

    city_sales = (
        sales.groupby("city", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    fig_city = px.bar(
        city_sales,
        x="city",
        y="revenue",
        color="city",
        labels={"revenue": "Revenue (₹)"}
    )

    st.plotly_chart(fig_city, use_container_width=True)

# Product performance
st.subheader("🏆 Top Performing Products")

product_sales = (
    sales.groupby("product_name", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        quantity_sold=("quantity", "sum")
    )
    .sort_values("revenue", ascending=False)
)

fig_products = px.bar(
    product_sales,
    x="product_name",
    y="revenue",
    color="revenue",
    title="Product-wise Revenue",
    labels={"revenue": "Revenue (₹)"}
)

st.plotly_chart(fig_products, use_container_width=True)

# Customer analysis
st.subheader("👥 Customer Analysis")

customer_sales = (
    sales.groupby(
        ["customer_name", "city"],
        as_index=False
    )
    .agg(
        revenue=("revenue", "sum"),
        orders=("order_id", "nunique")
    )
    .sort_values("revenue", ascending=False)
)

st.dataframe(
    customer_sales,
    use_container_width=True,
    hide_index=True
)

# Detailed sales data
with st.expander("View Detailed Sales Data"):
    st.dataframe(sales, use_container_width=True)

st.success("Retail Sales Analytics Dashboard loaded successfully!")
