/*
*****************************************************************************
FINAL DELIVERABLE
FINAL KPI SNAPSHOT

Use this result set for the final presentation / Power BI validation.

IMPORTANT:
    The numbers shown in the final presentation must come from executing this
    query against your actual SQL Server database.
******************************************************************************
*/

USE PRP_Ecommerce_Analytics;

WITH session_kpi AS
(
    SELECT
        COUNT(*) AS total_sessions,
        SUM(converted_session) AS converting_sessions
    FROM analytics.vw_session_funnel
),
order_kpi AS
(
    SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT user_id) AS ordering_users,
        SUM(items_purchased) AS units_sold,
        SUM(price_usd) AS gross_revenue,
        SUM(cogs_usd) AS cogs
    FROM analytics.vw_orders_clean
),
refund_kpi AS
(
    SELECT
        SUM(refund_amount_usd) AS refund_amount
    FROM analytics.vw_refunds_clean
)
SELECT
    s.total_sessions,
    s.converting_sessions,
    o.total_orders,
    o.ordering_users,
    o.units_sold,
    CAST(o.gross_revenue AS DECIMAL(18,2)) AS gross_revenue_usd,
    CAST(o.cogs AS DECIMAL(18,2)) AS cogs_usd,
    CAST(o.gross_revenue - o.cogs AS DECIMAL(18,2)) AS gross_profit_usd,
    CAST(
        (o.gross_revenue - o.cogs) * 100.0
        / NULLIF(o.gross_revenue,0)
        AS DECIMAL(10,2)
    ) AS gross_margin_pct,
    CAST(ISNULL(r.refund_amount,0) AS DECIMAL(18,2)) AS refund_amount_usd,
    CAST(
        o.gross_revenue - ISNULL(r.refund_amount,0)
        AS DECIMAL(18,2)
    ) AS net_revenue_usd,
    CAST(
        o.gross_revenue / NULLIF(o.total_orders,0)
        AS DECIMAL(18,2)
    ) AS aov_usd,
    CAST(
        s.converting_sessions * 100.0 / total_sessions
        AS DECIMAL(10,2)
    ) AS conversion_rate_pct,
    CAST(
        r.refund_amount* 100.0 / gross_revenue
        AS DECIMAL(10,2)
    ) AS refund_rate_pct,
    CAST(
        o.gross_revenue / s.total_sessions
        AS DECIMAL(18,2)
    ) AS revenue_per_session_usd
FROM session_kpi AS s
CROSS JOIN order_kpi AS o
CROSS JOIN refund_kpi AS r;

