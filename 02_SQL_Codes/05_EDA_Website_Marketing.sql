/*
------------------------------------------------------------------------------
FINAL DELIVERABLE
— WEBSITE FUNNEL & MARKETING EDA
------------------------------------------------------------------------------*/

USE PRP_Ecommerce_Analytics;


-- Website funnel

SELECT * FROM analytics.vw_session_funnel;

SELECT
    COUNT(*) AS Sessions,
    SUM(converted_session) AS converting_sessions,
    CAST(SUM(converted_session) * 100.0 / NULLIF(COUNT(*),0) AS DECIMAL(10,2)) AS Conversion_Rate_Pct,
    SUM(order_count) AS Orders,
    SUM(session_revenue) AS gross_revenue_usd
FROM analytics.vw_session_funnel;


-- Device performance

SELECT * FROM analytics.vw_session_funnel;

SELECT
    reporting_device_type AS Device_Type,
    COUNT(*) AS Sessions,
    SUM(converted_session) AS Converting_Sessions,
    SUM(converted_session) * 100.0 / COUNT(*)  AS Conversion_Rate_Pct,
    SUM(session_revenue) AS Revenue,
    SUM(session_revenue) / COUNT(*) AS Revenue_Per_Session
FROM analytics.vw_session_funnel
GROUP BY reporting_device_type
ORDER BY conversion_rate_pct DESC;


-- Repeat-session performance

SELECT * FROM analytics.vw_session_funnel;

SELECT
    CASE WHEN is_repeat_session = 1 THEN 'Repeat' ELSE 'New' END AS Session_Type,
    COUNT(*) AS Sessions,
    SUM(converted_session) AS Converting_Sessions,
    SUM(converted_session) * 100.0 / NULLIF(COUNT(*),0)  AS Conversion_Rate_Pct,
    SUM(session_revenue) AS Revenue
FROM analytics.vw_session_funnel
GROUP BY is_repeat_session
ORDER BY conversion_rate_pct DESC;


-- UTM source performance

SELECT
    reporting_utm_source AS utm_source,
    COUNT(*) AS Sessions,
    SUM(converted_session) AS Converting_Sessions,
    SUM(converted_session) * 100.0 / COUNT(*) AS Conversion_Rate_pct,
    SUM(session_revenue) AS revenue_usd,
    SUM(session_revenue) / COUNT(*) AS Revenue_per_session_usd
FROM analytics.vw_session_funnel
GROUP BY reporting_utm_source
ORDER BY revenue_usd DESC;


-- UTM campaign performance
SELECT
    UTM_Campaign,
    COUNT(*) AS Sessions,
    SUM(converted_session) AS Converting_Sessions,
    SUM(converted_session) * 100.0 / (COUNT(*)) AS Conversion_Rate_Pct,
    SUM(session_revenue) AS Revenue_usd
FROM analytics.vw_session_funnel
GROUP BY utm_campaign
ORDER BY revenue_usd DESC;


-- Pageviews per session

WITH pageview_counts AS(
 SELECT
     website_session_id,
     COUNT(*) AS pageviews
FROM analytics.vw_pageviews_clean
GROUP BY website_session_id
)
SELECT
    AVG(pageviews) AS avg_pageviews_per_session,
    MIN(pageviews) AS min_pageviews,
    MAX(pageviews) AS max_pageviews
FROM pageview_counts;


-- Page URL performance

SELECT TOP (25)
    Pageview_Url,
    COUNT(*) AS Pageviews,
    COUNT(DISTINCT website_session_id) AS Unique_Sessions
FROM analytics.vw_pageviews_clean
GROUP BY pageview_url
ORDER BY pageviews DESC;
