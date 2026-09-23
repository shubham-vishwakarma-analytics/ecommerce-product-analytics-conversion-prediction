/*
******************************************************************************
FINAL DELIVERABLE
 DIAGNOSTIC / BUSINESS ANALYSIS

Purpose:
    Move from "what happened?" to "where/why should management investigate?"

This file intentionally focuses on comparisons and decomposition rather than
claiming causal relationships that the observational data cannot prove.
********************************************************************************
*/

USE PRP_Ecommerce_Analytics;


-- Monthly revenue contribution by product 

SELECT
    DATEFROMPARTS(YEAR(oi.created_at),MONTH(oi.created_at),1) AS month_start,
    p.product_name,
    SUM(oi.price_usd) AS revenue_usd,
    CAST(SUM(oi.price_usd) * 100.0 / SUM(SUM(oi.price_usd)) OVER(PARTITION BY YEAR(oi.created_at),MONTH(oi.created_at)) AS DECIMAL(10,2)) AS revenue_share_pct
FROM analytics.vw_order_items_clean AS oi
INNER JOIN analytics.vw_products_clean AS p
    ON oi.product_id = p.product_id
GROUP BY
    DATEFROMPARTS(YEAR(oi.created_at),MONTH(oi.created_at),1),
    p.product_name,
    YEAR(oi.created_at),
    MONTH(oi.created_at)
ORDER BY month_start, revenue_usd DESC;


-- Conversion gap by device and repeat status 
SELECT
    reporting_device_type AS device_type,
    CASE WHEN is_repeat_session = 1 THEN 'Repeat' ELSE 'New' END AS session_type,
    COUNT(*) AS sessions,
    SUM(converted_session) AS converting_sessions,
    CAST(SUM(converted_session) * 100.0 / COUNT(*) AS DECIMAL(10,2)) AS conversion_rate_pct
FROM analytics.vw_session_funnel
GROUP BY
    reporting_device_type,
    is_repeat_session
ORDER BY conversion_rate_pct DESC;


-- Traffic quality matrix 
SELECT
    reporting_utm_source AS utm_source,
    COUNT(*) AS sessions,
    SUM(converted_session) AS converting_sessions,
    CAST(SUM(converted_session) * 100.0 / NULLIF(COUNT(*),0) AS DECIMAL(10,2)) AS conversion_rate_pct,
    CAST(SUM(session_revenue) AS DECIMAL(18,2)) AS revenue_usd,
    CAST(SUM(session_revenue) / NULLIF(COUNT(*),0) AS DECIMAL(18,2)) AS revenue_per_session_usd
FROM analytics.vw_session_funnel
GROUP BY reporting_utm_source
ORDER BY revenue_per_session_usd DESC;


-- Product performance matrix 
SELECT
    p.product_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    COUNT(*) AS units_sold,
    CAST(SUM(oi.price_usd) AS DECIMAL(18,2)) AS revenue_usd,
    CAST(SUM(oi.price_usd - oi.cogs_usd) AS DECIMAL(18,2)) AS gross_profit_usd,
    CAST(SUM(oi.price_usd - oi.cogs_usd) * 100.0  / NULLIF(SUM(oi.price_usd),0) AS DECIMAL(10,2)) AS margin_pct
FROM analytics.vw_order_items_clean AS oi
INNER JOIN analytics.vw_products_clean AS p
    ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue_usd DESC;


-- Orders by day of week
SELECT
    DATENAME(WEEKDAY, created_at) AS day_name,
    DATEPART(WEEKDAY, created_at) AS day_number,
    COUNT(DISTINCT order_id) AS orders,
    CAST(SUM(price_usd) AS DECIMAL(18,2)) AS revenue_usd
FROM analytics.vw_orders_clean
GROUP BY
    DATENAME(WEEKDAY, created_at),
    DATEPART(WEEKDAY, created_at)
ORDER BY day_number;

