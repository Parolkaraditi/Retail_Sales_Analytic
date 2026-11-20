
-- =========================================
-- RETAIL SALES ANALYTICS PROJECT
-- =========================================

CREATE DATABASE IF NOT EXISTS retail_sales_db;

USE retail_sales_db;

-- 1. View all tables
SHOW TABLES;

-- 2. View sample customer records
SELECT *
FROM customers
LIMIT 10;

-- 3. View sample orders
SELECT *
FROM orders
LIMIT 10;

-- 4. View order details
SELECT *
FROM orders_details
LIMIT 10;

-- 5. View product details
SELECT *
FROM products
LIMIT 10;


-- =========================================
-- BUSINESS ANALYSIS
-- =========================================

-- 6. Total customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM customers;

-- 7. Total orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- 8. Total products
SELECT COUNT(DISTINCT product_id) AS total_products
FROM products;

-- 9. Total quantity sold
SELECT SUM(quantity) AS total_quantity
FROM orders_details;

-- 10. Total sales
SELECT
    ROUND(SUM(quantity * unit_price), 2) AS total_sales
FROM orders_details;


-- =========================================
-- PRODUCT ANALYSIS
-- =========================================

-- 11. Sales by category
SELECT
    p.category,
    ROUND(SUM(od.quantity * od.unit_price), 2) AS total_sales
FROM orders_details od
JOIN products p
    ON od.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;


-- 12. Top 10 products
SELECT
    p.product_name,
    ROUND(SUM(od.quantity * od.unit_price), 2) AS total_sales
FROM orders_details od
JOIN products p
    ON od.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sales DESC
LIMIT 10;


-- 13. Quantity sold by product
SELECT
    p.product_name,
    SUM(od.quantity) AS total_quantity
FROM orders_details od
JOIN products p
    ON od.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity DESC;


-- =========================================
-- CUSTOMER ANALYSIS
-- =========================================

-- 14. Top 10 customers by sales
SELECT
    c.customer_id,
    c.customer_name,
    ROUND(SUM(od.quantity * od.unit_price), 2) AS total_sales
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN orders_details od
    ON o.order_id = od.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- 15. Orders by customer
SELECT
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_orders DESC;


-- =========================================
-- TIME-BASED ANALYSIS
-- =========================================

-- 16. Monthly sales
SELECT
    YEAR(o.order_date) AS order_year,
    MONTH(o.order_date) AS order_month,
    ROUND(SUM(od.quantity * od.unit_price), 2) AS total_sales
FROM orders o
JOIN orders_details od
    ON o.order_id = od.order_id
GROUP BY YEAR(o.order_date), MONTH(o.order_date)
ORDER BY order_year, order_month;


-- 17. Yearly sales
SELECT
    YEAR(o.order_date) AS order_year,
    ROUND(SUM(od.quantity * od.unit_price), 2) AS total_sales
FROM orders o
JOIN orders_details od
    ON o.order_id = od.order_id
GROUP BY YEAR(o.order_date)
ORDER BY order_year;


-- =========================================
-- ADVANCED ANALYSIS
-- =========================================

-- 18. Average order value
SELECT
    ROUND(AVG(order_total), 2) AS average_order_value
FROM (
    SELECT
        o.order_id,
        SUM(od.quantity * od.unit_price) AS order_total
    FROM orders o
    JOIN orders_details od
        ON o.order_id = od.order_id
    GROUP BY o.order_id
) AS order_summary;


-- 19. Repeat customers
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(DISTINCT o.order_id) > 1
ORDER BY order_count DESC;


-- 20. Products with no sales
SELECT
    p.product_id,
    p.product_name
FROM products p
LEFT JOIN orders_details od
    ON p.product_id = od.product_id
WHERE od.product_id IS NULL;
