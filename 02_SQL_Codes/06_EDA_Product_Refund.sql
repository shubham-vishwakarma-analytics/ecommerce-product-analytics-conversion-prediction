------------------------------------------------------------------------------
--FINAL DELIVERABLE
--PRODUCT & REFUND EDA
------------------------------------------------------------------------------

USE PRP_Ecommerce_Analytics;


-- Product sales, profit and margin

SELECT
    p.Product_id,
    p.Product_name,
    COUNT(DISTINCT oi.order_id) AS Orders,
    COUNT(*) AS Units_Sold,
    SUM(oi.price_usd) AS Revenue_usd,
    SUM(oi.cogs_usd) AS cogs_usd,
    SUM(oi.price_usd - oi.cogs_usd) AS Gross_Profit_usd,
    SUM(oi.price_usd - oi.cogs_usd) * 100.0 / SUM(oi.price_usd) AS Gross_Margin_pct
FROM analytics.vw_order_items_clean AS oi
INNER JOIN analytics.vw_products_clean AS p
    ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue_usd DESC;


-- Product refund exposure

WITH product_sales AS(
SELECT
    oi.product_id,
    SUM(oi.price_usd) AS Product_revenue
FROM analytics.vw_order_items_clean AS oi
GROUP BY oi.product_id
),
product_refunds AS(
SELECT
    oi.product_id,
    SUM(r.refund_amount_usd) AS refund_amount
FROM analytics.vw_refunds_clean AS r
JOIN analytics.vw_order_items_clean AS oi
        ON r.order_item_id = oi.order_item_id
GROUP BY oi.product_id
)
SELECT
    p.Product_id,
    p.Product_name,
    ps.Product_revenue AS Revenue_usd,
    pr.Refund_amount AS Refund_Amount_usd,
    pr.Refund_amount * 100.0 / ps.product_revenue AS Refund_Rate_Pct
FROM analytics.vw_products_clean AS p
LEFT JOIN product_sales AS ps
    ON p.product_id = ps.product_id
LEFT JOIN product_refunds AS pr
    ON p.product_id = pr.product_id
ORDER BY refund_rate_pct DESC;


-- Primary vs non-primary items

SELECT
    is_primary_item,
    COUNT(*) AS Item_rows,
    SUM(price_usd) AS Revenue_usd,
    SUM(cogs_usd) AS cogs_usd,
    SUM(price_usd - cogs_usd) AS Gross_Profit_usd
FROM analytics.vw_order_items_clean
GROUP BY is_primary_item
ORDER BY is_primary_item DESC;


-- Refunds by product
SELECT
    p.Product_id,
    p.Product_Name,
    COUNT(r.order_item_refund_id) AS Refund_Transactions,
    SUM(r.refund_amount_usd) AS Refund_Amount_usd
FROM analytics.vw_refunds_clean AS r
JOIN analytics.vw_order_items_clean AS oi
    ON r.order_item_id = oi.order_item_id
JOIN analytics.vw_products_clean AS p
    ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY refund_amount_usd DESC;
