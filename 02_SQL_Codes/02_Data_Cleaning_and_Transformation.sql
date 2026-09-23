/*
________________________________________________________________________________
FINAL DELIVERABLE
— DATA CLEANING AND TRANSFORMATION

Approach:
    Preserve raw tables.
    Build an analysis-ready layer in schema [analytics].

Why views?
    The project requires cleaning/transformation, but the source data should
    remain traceable. Views make the treatment reproducible and reversible.

Main treatments:
    - Preserve meaningful NULLs in raw data.
    - Create reporting categories for missing UTM values.
    - Normalize text fields with TRIM.
    - Expose derived profit/margin fields.
    - Create reusable session/order/product/refund analytical views.
________________________________________________________________________________*/

USE PRP_Ecommerce_Analytics;


CREATE SCHEMA analytics;

SELECT * FROM SYS.SCHEMAS
WHERE NAME = 'analytics';


/* ---------------------------------------------------------------------------
   1. Products
--------------------------------------------------------------------------- */
SELECT * FROM dbo.products;


CREATE OR ALTER VIEW analytics.vw_products_clean 
AS 
SELECT
    product_id,
    created_at,
    NULLIF(TRIM(product_name),'') AS product_name
FROM dbo.products;

SELECT * FROM analytics.vw_products_clean;
SELECT * FROM dbo.products;

/* ---------------------------------------------------------------------------
   2. Website sessions
--------------------------------------------------------------------------- */
SELECT * FROM dbo.website_sessions;


CREATE OR ALTER VIEW analytics.vw_sessions_clean
AS
SELECT
    website_session_id,
    created_at,
    user_id,
    is_repeat_session,
    NULLIF(TRIM(utm_source), '') AS utm_source,
    NULLIF(TRIM(utm_campaign), '') AS utm_campaign,
    NULLIF(TRIM(utm_content), '') AS utm_content,
    NULLIF(TRIM(device_type), '') AS device_type,
    NULLIF(TRIM(http_referer), '') AS http_referer,
    CASE
        WHEN NULLIF(TRIM(utm_source), '') IS NULL THEN 'UNTRACKED' ELSE TRIM(utm_source) END AS reporting_utm_source, 
    CASE
        WHEN NULLIF(TRIM(device_type), '') IS NULL THEN 'UNKNOWN' ELSE LOWER(TRIM(device_type)) END AS reporting_device_type
FROM dbo.website_sessions;

SELECT * FROM analytics.vw_sessions_clean;
SELECT * FROM dbo.website_sessions;



/* ---------------------------------------------------------------------------
   3. Pageviews
--------------------------------------------------------------------------- */
SELECT * FROM dbo.website_pageviews;


CREATE OR ALTER VIEW analytics.vw_pageviews_clean
AS
SELECT
    website_pageview_id,
    created_at,
    website_session_id,
    NULLIF(TRIM(pageview_url), '') AS pageview_url
FROM dbo.website_pageviews;

SELECT * FROM analytics.vw_pageviews_clean;
SELECT * FROM dbo.website_pageviews;


/* ---------------------------------------------------------------------------
   4. Orders
--------------------------------------------------------------------------- */
SELECT * FROM dbo.orders;

CREATE OR ALTER VIEW analytics.vw_orders_clean
AS
SELECT
    order_id,
    created_at,
    website_session_id,
    user_id,
    primary_product_id,
    items_purchased,
    CAST(price_usd AS DECIMAL(18,2)) AS price_usd,
    CAST(cogs_usd AS DECIMAL(18,2)) AS cogs_usd,
    CAST(price_usd - cogs_usd AS DECIMAL(18,2)) AS gross_profit_usd,
    CASE
        WHEN price_usd > 0 THEN CAST((price_usd - cogs_usd) * 100.0 / price_usd AS DECIMAL(10,2)) ELSE NULL END AS gross_margin_pct
FROM dbo.orders;

SELECT * FROM analytics.vw_orders_clean;
SELECT * FROM dbo.orders;

/* ---------------------------------------------------------------------------
   5. Order items
--------------------------------------------------------------------------- */
SELECT * FROM dbo.order_items;

CREATE OR ALTER VIEW analytics.vw_order_items_clean
AS
SELECT
    order_item_id,
    created_at,
    order_id,
    product_id,
    is_primary_item,
    CAST(price_usd AS DECIMAL(18,2)) AS price_usd,
    CAST(cogs_usd AS DECIMAL(18,2)) AS cogs_usd,
    CAST(price_usd - cogs_usd AS DECIMAL(18,2)) AS gross_profit_usd
FROM dbo.order_items;

SELECT * FROM analytics.vw_order_items_clean;
SELECT * FROM dbo.order_items;


/* ---------------------------------------------------------------------------
   6. Refunds
--------------------------------------------------------------------------- */
SELECT * FROM dbo.order_item_refunds;

CREATE OR ALTER VIEW analytics.vw_refunds_clean
AS
SELECT
    order_item_refund_id,
    created_at,
    order_item_id,
    order_id,
    CAST(refund_amount_usd AS DECIMAL(18,2)) AS refund_amount_usd
FROM dbo.order_item_refunds;

SELECT * FROM analytics.vw_refunds_clean;
SELECT * FROM dbo.order_item_refunds;


/* ---------------------------------------------------------------------------
   7. Session-level conversion layer
   A session is converted when at least one order is linked to it.
--------------------------------------------------------------------------- */

SELECT * FROM dbo.website_sessions;


CREATE OR ALTER VIEW analytics.vw_session_funnel
AS
SELECT
    s.website_session_id,
    s.created_at,
    s.user_id,
    s.is_repeat_session,
    s.reporting_utm_source,
    s.utm_campaign,
    s.utm_content,
    s.reporting_device_type,
    s.http_referer,
    CASE WHEN o.order_count > 0 THEN 1 ELSE 0 END AS converted_session, 
    ISNULL(o.order_count,0) AS order_count,
    ISNULL(o.session_revenue,0) AS session_revenue
FROM analytics.vw_sessions_clean AS s
LEFT JOIN(
SELECT
    website_session_id,
    COUNT(*) AS order_count,
    SUM(price_usd) AS session_revenue
FROM analytics.vw_orders_clean
GROUP BY website_session_id
) AS o
    ON s.website_session_id = o.website_session_id;


SELECT * FROM analytics.vw_session_funnel;

SELECT * FROM dbo.website_sessions;
SELECT * FROM analytics.vw_orders_clean;
