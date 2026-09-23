/*
-----------------------------------------------------------------------------
FINAL DELIVERABLE
FINAL DATA QUALITY & BUSINESS RECONCILIATION

Purpose:
    Prove that the analytical layer is internally consistent before it is
    consumed by Power BI/Python.
-----------------------------------------------------------------------------
*/

USE PRP_Ecommerce_Analytics;


-- Orders vs order items 
WITH item_summary AS
(
    SELECT
        order_id,
        COUNT(*) AS item_count,
        SUM(price_usd) AS item_revenue,
        SUM(cogs_usd) AS item_cogs
    FROM analytics.vw_order_items_clean
    GROUP BY order_id
)
SELECT
    COUNT(*) AS total_orders_checked,
    SUM(CASE WHEN o.items_purchased = i.item_count
         AND ABS(o.price_usd - i.item_revenue) <= 0.01
         AND ABS(o.cogs_usd - i.item_cogs) <= 0.01
        THEN 1 ELSE 0 END) AS reconciled_orders,
    SUM(CASE
        WHEN o.items_purchased <> i.item_count
          OR ABS(o.price_usd - i.item_revenue) > 0.01
          OR ABS(o.cogs_usd - i.item_cogs) > 0.01
        THEN 1 ELSE 0 END) AS unreconciled_orders
FROM analytics.vw_orders_clean AS o
LEFT JOIN item_summary AS i
    ON o.order_id = i.order_id;


-- Refunds vs eligible item revenue 
SELECT
    COUNT(*) AS refund_rows_checked,
    SUM(CASE WHEN r.refund_amount_usd <= oi.price_usd THEN 1 ELSE 0 END) AS valid_refund_rows,
    SUM(CASE WHEN r.refund_amount_usd > oi.price_usd THEN 1 ELSE 0 END) AS over_refund_rows
FROM analytics.vw_refunds_clean AS r
INNER JOIN analytics.vw_order_items_clean AS oi
    ON r.order_item_id = oi.order_item_id;


-- Session-to-order relationship
SELECT
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT o.website_session_id) AS sessions_with_orders,
    SUM(CASE WHEN s.website_session_id IS NOT NULL THEN 1 ELSE 0 END) AS orders_with_valid_session
FROM analytics.vw_orders_clean AS o
LEFT JOIN analytics.vw_sessions_clean AS s
    ON o.website_session_id = s.website_session_id;


-- Product relationship 
SELECT
    COUNT(*) AS order_item_rows,
    SUM(CASE WHEN p.product_id IS NOT NULL THEN 1 ELSE 0 END) AS items_with_valid_product,
    SUM(CASE WHEN p.product_id IS NULL THEN 1 ELSE 0 END) AS orphan_product_items
FROM analytics.vw_order_items_clean AS oi
LEFT JOIN analytics.vw_products_clean AS p
    ON oi.product_id = p.product_id;
GO

-- Timestamp sequence checks 
SELECT
    'Pageview before session' AS check_name,
    COUNT(*) AS issue_count
FROM analytics.vw_pageviews_clean AS pv
INNER JOIN analytics.vw_sessions_clean AS s
    ON pv.website_session_id = s.website_session_id
WHERE pv.created_at < s.created_at

UNION ALL

SELECT
    'Order before session',
    COUNT(*)
FROM analytics.vw_orders_clean AS o
INNER JOIN analytics.vw_sessions_clean AS s
    ON o.website_session_id = s.website_session_id
WHERE o.created_at < s.created_at

UNION ALL

SELECT
    'Refund before order item',
    COUNT(*)
FROM analytics.vw_refunds_clean AS r
INNER JOIN analytics.vw_order_items_clean AS oi
    ON r.order_item_id = oi.order_item_id
WHERE r.created_at < oi.created_at;

