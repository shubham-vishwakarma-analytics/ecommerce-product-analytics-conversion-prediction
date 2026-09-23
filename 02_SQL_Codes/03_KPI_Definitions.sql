------------------------------------------------------------
------------— KPI Definitions----------------------
------------------------------------------------------------

USE PRP_Ecommerce_Analytics;

SELECT * FROM analytics.vw_order_items_clean
SELECT * FROM analytics.vw_orders_clean;
SELECT * FROM analytics.vw_pageviews_clean;
SELECT * FROM analytics.vw_sessions_clean;
SELECT * FROM analytics.vw_refunds_clean;
SELECT * FROM analytics.vw_products_clean;




--Overall Sales KPIs

SELECT
    COUNT(DISTINCT order_id) AS Total_Orders,
    SUM(items_purchased) AS Total_units_sold,
    SUM(price_usd) AS Gross_Revenue,
    SUM(cogs_usd) AS Total_cogs,
    SUM(price_usd - cogs_usd) AS Gross_Profit
FROM analytics.vw_orders_clean;


--Gross Margin %

SELECT 
    CAST(
    SUM(price_usd - cogs_usd)*100.0 
    / SUM(price_usd) AS DECIMAL(20,2)) AS Gross_Margin_Percentage
FROM analytics.vw_order_items_clean;


--Average Order Values - AOV

SELECT 
    CAST(AVG(price_usd) AS DECIMAL(20,2)) AS AOV 
FROM analytics.vw_orders_clean;


--Refund Amount

SELECT 
    SUM(refund_amount_usd) AS Total_Refund_Amount
FROM analytics.vw_refunds_clean;


-- Net Revenue 
SELECT
    (SELECT SUM(price_usd) FROM  analytics.vw_orders_clean) -
    (SELECT SUM(refund_amount_usd) FROM analytics.vw_refunds_clean)
AS Net_Revenue;


--Total Website Sessions

SELECT
    COUNT(*) AS Total_Sessions
FROM analytics.vw_session_funnel;



SELECT * FROM analytics.vw_order_items_clean
SELECT * FROM analytics.vw_orders_clean;
SELECT * FROM analytics.vw_pageviews_clean;
SELECT * FROM analytics.vw_sessions_clean;
SELECT * FROM analytics.vw_refunds_clean;
SELECT * FROM analytics.vw_products_clean;