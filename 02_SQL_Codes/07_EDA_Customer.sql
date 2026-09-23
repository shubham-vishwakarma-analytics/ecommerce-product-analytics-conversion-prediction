/*
******************************************************************************
FINAL DELIVERABLE
 — CUSTOMER / USER EDA
*******************************************************************************/

USE PRP_Ecommerce_Analytics;
GO

-- 1. Customer order frequency 
WITH customer_orders AS
(
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(price_usd) AS revenue_usd
    FROM analytics.vw_orders_clean
    GROUP BY user_id
)
SELECT
    COUNT(*) AS ordering_customers,
    AVG(CAST(order_count AS DECIMAL(18,2))) AS avg_orders_per_customer,
    CAST(SUM(revenue_usd) AS DECIMAL(18,2)) AS total_customer_revenue_usd,
    CAST(AVG(revenue_usd) AS DECIMAL(18,2)) AS avg_revenue_per_ordering_customer
FROM customer_orders;

-- New vs repeat session behaviour 
SELECT
    CASE WHEN is_repeat_session = 1 THEN 'Repeat Session'
         ELSE 'New Session'
    END AS session_type,
    COUNT(*) AS sessions,
    SUM(converted_session) AS converting_sessions,
    CAST(
        SUM(converted_session) * 100.0 / NULLIF(COUNT(*),0)
        AS DECIMAL(10,2)
    ) AS conversion_rate_pct,
    CAST(SUM(session_revenue) AS DECIMAL(18,2)) AS revenue_usd
FROM analytics.vw_session_funnel
GROUP BY is_repeat_session
ORDER BY conversion_rate_pct DESC;


-- Users with multiple orders 
WITH user_orders AS
(
    SELECT
        user_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(price_usd) AS revenue_usd
    FROM analytics.vw_orders_clean
    GROUP BY user_id
)
SELECT
    COUNT(*) AS repeat_ordering_users,
    CAST(SUM(revenue_usd) AS DECIMAL(18,2)) AS repeat_user_revenue_usd
FROM user_orders
WHERE order_count > 1;


-- Top customers by revenue 
SELECT TOP (25)
    user_id,
    COUNT(DISTINCT order_id) AS orders,
    CAST(SUM(price_usd) AS DECIMAL(18,2)) AS revenue_usd,
    CAST(SUM(price_usd - cogs_usd) AS DECIMAL(18,2)) AS gross_profit_usd
FROM analytics.vw_orders_clean
GROUP BY user_id
ORDER BY revenue_usd DESC;

