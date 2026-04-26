-- ============================================================
-- Sales Insights Project — SQL Analysis Queries
-- AtliQ Hardware | Codebasics Project
-- ============================================================
USE sales_insights_db;

-- ── Q1: Total Revenue ──────────────────────────────────────────
SELECT
    ROUND(SUM(sales_amount)/10000000, 2) AS total_revenue_cr
FROM transactions;

-- ── Q2: Revenue by year ────────────────────────────────────────
SELECT
    d.year,
    ROUND(SUM(t.sales_amount)/10000000, 2) AS revenue_cr
FROM transactions t
JOIN date d ON t.order_date = d.date
GROUP BY d.year
ORDER BY d.year;

-- ── Q3: Revenue in 2020 ────────────────────────────────────────
SELECT
    ROUND(SUM(t.sales_amount)/10000000, 2) AS revenue_2020_cr
FROM transactions t
JOIN date d ON t.order_date = d.date
WHERE d.year = 2020;

-- ── Q4: Top 5 customers by revenue ────────────────────────────
SELECT
    c.custmer_name,
    c.customer_type,
    ROUND(SUM(t.sales_amount)/1000000, 2) AS revenue_mn
FROM transactions t
JOIN customers c ON t.customer_code = c.customer_code
GROUP BY c.custmer_name, c.customer_type
ORDER BY revenue_mn DESC
LIMIT 5;

-- ── Q5: Top 5 markets by revenue ──────────────────────────────
SELECT
    m.markets_name,
    m.zone,
    ROUND(SUM(t.sales_amount)/1000000, 2) AS revenue_mn
FROM transactions t
JOIN markets m ON t.market_code = m.markets_code
WHERE m.markets_code NOT IN ('Mark097','Mark098')
GROUP BY m.markets_name, m.zone
ORDER BY revenue_mn DESC
LIMIT 5;

-- ── Q6: Revenue by zone ────────────────────────────────────────
SELECT
    m.zone,
    ROUND(SUM(t.sales_amount)/10000000, 2) AS revenue_cr,
    ROUND(SUM(t.profit_margin)/10000000, 2) AS profit_cr
FROM transactions t
JOIN markets m ON t.market_code = m.markets_code
WHERE m.markets_code NOT IN ('Mark097','Mark098')
GROUP BY m.zone
ORDER BY revenue_cr DESC;

-- ── Q7: Monthly revenue trend 2020 ────────────────────────────
SELECT
    d.month_name,
    ROUND(SUM(t.sales_amount)/1000000, 2) AS revenue_mn
FROM transactions t
JOIN date d ON t.order_date = d.date
WHERE d.year = 2020
GROUP BY d.month_name, MONTH(d.date)
ORDER BY MONTH(d.date);

-- ── Q8: Profit margin by market ────────────────────────────────
SELECT
    m.markets_name,
    ROUND(AVG(t.profit_margin_percentage), 2) AS avg_margin_pct,
    ROUND(SUM(t.profit_margin)/1000000, 2)    AS total_profit_mn
FROM transactions t
JOIN markets m ON t.market_code = m.markets_code
WHERE m.markets_code NOT IN ('Mark097','Mark098')
GROUP BY m.markets_name
ORDER BY avg_margin_pct DESC;

-- ── Q9: Own Brand vs Distribution ─────────────────────────────
SELECT
    p.product_type,
    COUNT(*)                                   AS total_orders,
    ROUND(SUM(t.sales_amount)/10000000, 2)     AS revenue_cr,
    ROUND(AVG(t.profit_margin_percentage), 2)  AS avg_margin_pct
FROM transactions t
JOIN products p ON t.product_code = p.product_code
GROUP BY p.product_type;

-- ── Q10: Brick & Mortar vs E-Commerce ─────────────────────────
SELECT
    c.customer_type,
    ROUND(SUM(t.sales_amount)/10000000, 2) AS revenue_cr,
    ROUND(SUM(t.profit_margin)/10000000,2) AS profit_cr,
    COUNT(*) AS total_orders
FROM transactions t
JOIN customers c ON t.customer_code = c.customer_code
GROUP BY c.customer_type;

-- ── Q11: Revenue normalisation check (no USD) ─────────────────
SELECT
    currency,
    COUNT(*) AS cnt,
    ROUND(SUM(sales_amount)/10000000,2) AS revenue_cr
FROM transactions
GROUP BY currency;

-- ── Q12: Year-on-year growth ───────────────────────────────────
SELECT
    d.year,
    ROUND(SUM(t.sales_amount)/10000000, 2) AS revenue_cr,
    ROUND(SUM(t.profit_margin)/10000000, 2) AS profit_cr,
    ROUND(AVG(t.profit_margin_percentage), 2) AS avg_margin
FROM transactions t
JOIN date d ON t.order_date = d.date
GROUP BY d.year
ORDER BY d.year;
