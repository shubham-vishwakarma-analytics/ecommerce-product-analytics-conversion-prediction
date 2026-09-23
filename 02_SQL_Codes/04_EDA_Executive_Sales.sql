/*
-----------------------------------------------------------------------------
FINAL DELIVERABLE
EXECUTIVE / SALES EDA

Questions:
    How is the business performing?
    How do revenue, orders, profit and refunds change over time?
-----------------------------------------------------------------------------
*/

USE PRP_Ecommerce_Analytics;


-- Overall executive KPI 

SELECT * FROM analytics.vw_orders_clean;


SELECT
    COUNT(DISTINCT order_id) AS Orders,
    SUM(items_purchased) AS Units_Sold,
    CAST(SUM(price_usd) AS DECIMAL(18,2)) AS Gross_Revenue,
    CAST(SUM(cogs_usd) AS DECIMAL(18,2)) AS Total_cogs_usd,
    CAST(SUM(price_usd - cogs_usd) AS DECIMAL(18,2)) AS Gross_Profit_usd,
    CAST(SUM(price_usd - cogs_usd) * 100.0 / SUM(price_usd) AS DECIMAL(10,2)) AS Gross_Margin_pct,
    CAST(SUM(price_usd) * 1.0 / COUNT(DISTINCT order_id) AS DECIMAL(18,2)) AS AOV_usd
FROM analytics.vw_orders_clean;


-- Monthly Sales Trends

SELECT * FROM analytics.vw_orders_clean;

SELECT 
    YEAR(created_at) AS Year,
    MONTH(created_at) AS Months,
    SUM(DISTINCT order_id) AS Total_Orders,
    SUM(price_usd) AS Total_Sales,
    SUM(gross_profit_usd) AS Total_Gross_Profit,
    SUM(cogs_usd) AS Total_COGS,
    SUM(price_usd - cogs_usd) AS Total_Gross_Profit,
    CAST(SUM(price_usd - cogs_usd)*100 / SUM(price_usd) AS DECIMAL(10,2)) AS Total_Gross_Margin
FROM analytics.vw_orders_clean
GROUP BY YEAR(created_at), MONTH(created_at)
ORDER BY YEAR(created_at), MONTH(created_at);


-- Refund Trend

SELECT * FROM analytics.vw_refunds_clean;

SELECT
    YEAR(created_at) AS Year,
    MONTH(created_at) AS Months,
    SUM(DISTINCT order_item_refund_id) AS Total_Returned_Orders,
    SUM(refund_amount_usd) AS Total_Refun_Amounts
FROM analytics.vw_refunds_clean
GROUP BY YEAR(created_at), MONTH(created_at)
ORDER BY YEAR(created_at), MONTH(created_at);


-- Daily order/revenue trend

SELECT
    CAST(created_at AS DATE) AS Sales_Date,
    COUNT(DISTINCT order_id) AS Total_Orders,
    SUM(price_usd) AS Total_Revenue,
    SUM(price_usd - cogs_usd)  AS Total_Gross_Profit
FROM analytics.vw_orders_clean
GROUP BY CAST(created_at AS DATE)
ORDER BY sales_date;
