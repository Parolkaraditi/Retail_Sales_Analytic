USE retail_sales_db;
USE retail_sales;

DESCRIBE orders;
SHOW TABLES;
DESCRIBE customers;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE orders_details;
SELECT *
FROM orders_details
LIMIT 10;


USE retail_sales;

-- 1. Total Revenue
SELECT
    SUM(quantity * unit_price) AS total_revenue
FROM orders_details;

-- 2. Total Orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- 3. Total Customers
SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM orders;

-- 4. Total Products
SELECT
    COUNT(*) AS total_products
FROM products;

-- 5. Category-wise Revenue
SELECT
    p.category,
    SUM(od.quantity * od.unit_price) AS total_revenue
FROM orders_details od
JOIN products p
    ON od.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 6. Top 5 Best-Selling Products
SELECT
    p.product_name,
    SUM(od.quantity) AS total_quantity,
    SUM(od.quantity * od.unit_price) AS total_revenue
FROM orders_details od
JOIN products p
    ON od.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
LIMIT 5;

-- 7. City-wise Revenue
SELECT
    c.city,
    SUM(od.quantity * od.unit_price) AS total_revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN orders_details od
    ON o.order_id = od.order_id
GROUP BY c.city
ORDER BY total_revenue DESC;
