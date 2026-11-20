USE retail_sales;

-- 1. Rank Customers by Revenue

SELECT
    c.customer_name,
    SUM(od.quantity * od.unit_price) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(od.quantity * od.unit_price) DESC
    ) AS customer_rank
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN orders_details od
    ON o.order_id = od.order_id
GROUP BY c.customer_id, c.customer_name;

-- 2. Rank Products by Revenue

SELECT
    p.product_name,
    p.category,
    SUM(od.quantity * od.unit_price) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(od.quantity * od.unit_price) DESC
    ) AS product_rank
FROM products p
JOIN orders_details od
    ON p.product_id = od.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category;
    
    -- 3. Rank Products Within Each Category

SELECT
    p.product_name,
    p.category,
    SUM(od.quantity * od.unit_price) AS total_revenue,

    DENSE_RANK() OVER (
        PARTITION BY p.category
        ORDER BY SUM(od.quantity * od.unit_price) DESC
    ) AS category_rank

FROM products p
JOIN orders_details od
    ON p.product_id = od.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category;
    
    -- Customer Segmentation Based on Revenue

SELECT
    c.customer_name,
    SUM(od.quantity * od.unit_price) AS total_spending,

    CASE
        WHEN SUM(od.quantity * od.unit_price) >= 50000
            THEN 'High Value Customer'
        WHEN SUM(od.quantity * od.unit_price) >= 10000
            THEN 'Medium Value Customer'
        ELSE 'Low Value Customer'
    END AS customer_segment

FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN orders_details od
    ON o.order_id = od.order_id

GROUP BY
    c.customer_id,
    c.customer_name

ORDER BY total_spending DESC;


-- 4. Month-over-Month Revenue Growth

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(
            STR_TO_DATE(o.order_date, '%Y-%m-%d'),
            '%Y-%m'
        ) AS order_month,
        SUM(od.quantity * od.unit_price) AS revenue
    FROM orders o
    JOIN orders_details od
        ON o.order_id = od.order_id
    GROUP BY order_month
),

revenue_growth AS (
    SELECT
        order_month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY order_month
        ) AS previous_month_revenue
    FROM monthly_sales
)

SELECT
    order_month,
    revenue,
    previous_month_revenue,
    ROUND(
        (revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0) * 100,
        2
    ) AS growth_percentage
FROM revenue_growth
ORDER BY order_month;


-- 5. Repeat vs One-Time Customer Analysis

SELECT
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,

    CASE
        WHEN COUNT(DISTINCT o.order_id) > 1
            THEN 'Repeat Customer'
        ELSE 'One-Time Customer'
    END AS customer_type

FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id

GROUP BY
    c.customer_id,
    c.customer_name

ORDER BY total_orders DESC;


-- 6. Category-wise Revenue Contribution

SELECT
    p.category,
    SUM(od.quantity * od.unit_price) AS category_revenue,

    ROUND(
        SUM(od.quantity * od.unit_price) * 100.0 /
        (SELECT SUM(quantity * unit_price)
         FROM orders_details),
        2
    ) AS revenue_contribution_percentage

FROM products p
JOIN orders_details od
    ON p.product_id = od.product_id

GROUP BY p.category
ORDER BY category_revenue DESC;


