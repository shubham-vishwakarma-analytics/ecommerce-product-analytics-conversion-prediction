/*
---------------------------------------------------------------------------
E-COMMERCE DIGITAL ANALYTICS PROJECT
FINAL DELIVERABLE
01 — FINAL AUDIT REVALIDATION

Purpose:
    Reconfirm the important data-quality findings identified during the
    First Deliverable before applying any analytical transformation.

Principle:
    Raw source tables are NOT modified.

Database:
    PRP_Ecommerce_Analytics
------------------------------------------------------------------------------*/

USE PRP_Ecommerce_Analytics;


-- 1. Table inventory and row counts

SELECT 'Orders' AS Table_Name, COUNT(*) AS Total_Rows FROM orders
UNION
SELECT 'Products' AS Table_Name, COUNT(*) AS Total_Rows FROM products
UNION
SELECT 'order_items' AS Table_Name, COUNT(*) AS Total_Rows FROM order_items
UNION
SELECT 'order_item_refunds' AS Table_Name, COUNT(*) AS Total_Rows FROM order_item_refunds
UNION
SELECT 'website_sessions' AS Table_Name, COUNT(*) AS Total_Rows FROM website_sessions
UNION
SELECT 'website_pageviews' AS Table_Name, COUNT(*) AS Total_Rows FROM website_pageviews
ORDER BY Table_Name;


-- 2. Primary/business-key duplicate checks


SELECT product_id, COUNT(*) AS record_count
FROM dbo.products
GROUP BY product_id
HAVING COUNT(*) > 1;


SELECT website_session_id, COUNT(*) AS record_count
FROM dbo.website_sessions
GROUP BY website_session_id
HAVING COUNT(*) > 1;


SELECT website_pageview_id, COUNT(*) AS record_count
FROM dbo.website_pageviews
GROUP BY website_pageview_id
HAVING COUNT(*) > 1;


SELECT order_id, COUNT(*) AS record_count
FROM dbo.orders
GROUP BY order_id
HAVING COUNT(*) > 1;


SELECT order_item_id, COUNT(*) AS record_count
FROM dbo.order_items
GROUP BY order_item_id
HAVING COUNT(*) > 1;


SELECT order_item_refund_id, COUNT(*) AS record_count
FROM dbo.order_item_refunds
GROUP BY order_item_refund_id
HAVING COUNT(*) > 1;



-- 3. Meaningful NULL review — UTM/referrer fields are allowed to be NULL.


SELECT
    COUNT(*) AS total_sessions,
    SUM(CASE WHEN utm_source IS NULL THEN 1 ELSE 0 END) AS null_utm_source,
    SUM(CASE WHEN utm_campaign IS NULL THEN 1 ELSE 0 END) AS null_utm_campaign,
    SUM(CASE WHEN utm_content IS NULL THEN 1 ELSE 0 END) AS null_utm_content,
    SUM(CASE WHEN http_referer IS NULL THEN 1 ELSE 0 END) AS null_http_referer
FROM dbo.website_sessions;


-- 4. Invalid numeric/flag values 


SELECT *
FROM dbo.orders
WHERE items_purchased < 1
   OR price_usd < 0
   OR cogs_usd < 0
   OR cogs_usd > price_usd;


SELECT *
FROM dbo.order_items
WHERE price_usd < 0
   OR cogs_usd < 0
   OR cogs_usd > price_usd;


SELECT *
FROM dbo.order_item_refunds
WHERE refund_amount_usd <= 0;


SELECT *
FROM dbo.website_sessions
WHERE is_repeat_session NOT IN (0,1);


SELECT *
FROM dbo.order_items
WHERE is_primary_item NOT IN (0,1);


-- 5. Referential-integrity checks 


SELECT o.order_id, o.website_session_id
FROM dbo.orders AS o
LEFT JOIN dbo.website_sessions AS s
    ON o.website_session_id = s.website_session_id
WHERE s.website_session_id IS NULL;


SELECT o.order_id, o.primary_product_id
FROM dbo.orders AS o
LEFT JOIN dbo.products AS p
    ON o.primary_product_id = p.product_id
WHERE p.product_id IS NULL;


SELECT oi.order_item_id, oi.order_id
FROM dbo.order_items AS oi
LEFT JOIN dbo.orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


SELECT oi.order_item_id, oi.product_id
FROM dbo.order_items AS oi
LEFT JOIN dbo.products AS p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;



SELECT r.order_item_refund_id, r.order_item_id
FROM dbo.order_item_refunds AS r
LEFT JOIN dbo.order_items AS oi
    ON r.order_item_id = oi.order_item_id
WHERE oi.order_item_id IS NULL;


SELECT r.order_item_refund_id, r.order_id
FROM dbo.order_item_refunds AS r
LEFT JOIN dbo.orders AS o
    ON r.order_id = o.order_id
WHERE o.order_id IS NULL;


SELECT pv.website_pageview_id, pv.website_session_id
FROM dbo.website_pageviews AS pv
LEFT JOIN dbo.website_sessions AS s
    ON pv.website_session_id = s.website_session_id
WHERE s.website_session_id IS NULL;


-- 6. Order to item reconciliation 


WITH item_summary AS
(
    SELECT
        order_id,
        COUNT(*) AS item_row_count,
        SUM(price_usd) AS item_revenue,
        SUM(cogs_usd) AS item_cogs,
        SUM(CASE WHEN is_primary_item = 1 THEN 1 ELSE 0 END) AS primary_item_count
    FROM dbo.order_items
    GROUP BY order_id
)
SELECT
    o.order_id,
    o.items_purchased,
    i.item_row_count,
    o.price_usd AS order_revenue,
    i.item_revenue,
    o.cogs_usd AS order_cogs,
    i.item_cogs,
    i.primary_item_count
FROM dbo.orders AS o
LEFT JOIN item_summary AS i
    ON o.order_id = i.order_id
WHERE o.items_purchased <> ISNULL(i.item_row_count,0)
   OR ABS(o.price_usd - ISNULL(i.item_revenue,0)) > 0.01
   OR ABS(o.cogs_usd - ISNULL(i.item_cogs,0)) > 0.01
   OR ISNULL(i.primary_item_count,0) <> 1;


-- 7. Refund-to-item and refund-to-order consistency 


SELECT
    r.order_item_refund_id,
    r.order_id AS refund_order_id,
    oi.order_id AS item_order_id,
    r.refund_amount_usd,
    oi.price_usd AS item_price
FROM dbo.order_item_refunds AS r
INNER JOIN dbo.order_items AS oi
    ON r.order_item_id = oi.order_item_id
WHERE r.order_id <> oi.order_id
   OR r.refund_amount_usd > oi.price_usd;
