-- ============================================================
-- Sales Insights Project — AtliQ Hardware Company
-- Inspired by Codebasics Data Analysis Project
-- Database: sales_insights_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS sales_insights_db;
USE sales_insights_db;

-- ── Customers table ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customers (
    customer_code VARCHAR(10) PRIMARY KEY,
    custmer_name  VARCHAR(100),
    customer_type VARCHAR(20)
);

INSERT INTO customers VALUES
('Cus001','Surge Stores','Brick & Mortar'),
('Cus002','Nomad Stores','Brick & Mortar'),
('Cus003','Excel Stores','Brick & Mortar'),
('Cus004','Surface Stores','Brick & Mortar'),
('Cus005','Premium Stores','Brick & Mortar'),
('Cus006','Nixon','E-Commerce'),
('Cus007','Sage','E-Commerce'),
('Cus008','Electricalsara Stores','Brick & Mortar'),
('Cus009','Electricalslytical','E-Commerce'),
('Cus010','Electricalsbea Stores','Brick & Mortar'),
('Cus011','Info Stores','Brick & Mortar'),
('Cus012','Synthetic','E-Commerce'),
('Cus013','Path','E-Commerce'),
('Cus014','Logic Stores','Brick & Mortar'),
('Cus015','Leader','E-Commerce'),
('Cus016','Propel','E-Commerce'),
('Cus017','Sunset','E-Commerce'),
('Cus018','Control','E-Commerce'),
('Cus019','Epic Stores','Brick & Mortar'),
('Cus020','Novus','E-Commerce');

-- ── Products table ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
    product_code VARCHAR(10) PRIMARY KEY,
    product_type VARCHAR(20)
);

INSERT INTO products VALUES
('Prod001','Own Brand'),
('Prod002','Own Brand'),
('Prod003','Own Brand'),
('Prod004','Own Brand'),
('Prod005','Own Brand'),
('Prod006','Distribution'),
('Prod007','Distribution'),
('Prod008','Distribution'),
('Prod009','Own Brand'),
('Prod010','Distribution'),
('Prod011','Own Brand'),
('Prod012','Distribution'),
('Prod013','Own Brand'),
('Prod014','Distribution'),
('Prod015','Own Brand'),
('Prod016','Distribution'),
('Prod017','Own Brand'),
('Prod018','Distribution');

-- ── Markets (zones) table ────────────────────────────────────
CREATE TABLE IF NOT EXISTS markets (
    markets_code VARCHAR(10) PRIMARY KEY,
    markets_name VARCHAR(100),
    zone          VARCHAR(20)
);

INSERT INTO markets VALUES
('Mark001','Chennai','South'),
('Mark002','Mumbai','Central'),
('Mark003','Ahmedabad','North'),
('Mark004','Delhi NCR','North'),
('Mark005','Kanpur','North'),
('Mark006','Bengaluru','South'),
('Mark007','Bhopal','Central'),
('Mark008','Lucknow','North'),
('Mark009','Patna','Central'),
('Mark010','Surat','North'),
('Mark011','Nagpur','Central'),
('Mark012','Hyderabad','South'),
('Mark013','Bhubaneswar','South'),
('Mark014','Kochi','South'),
('Mark015','Pune','Central'),
('Mark097','New York','North America'),
('Mark098','Paris','Europe');

-- ── Date table ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS date (
    date       DATE PRIMARY KEY,
    cy_date    DATE,
    year       INT,
    month_name VARCHAR(20),
    date_yy_mmm VARCHAR(10)
);

-- Insert 2 years of dates (2018-2020)
INSERT INTO date
SELECT
    d,
    DATE_SUB(d, INTERVAL 1 YEAR),
    YEAR(d),
    MONTHNAME(d),
    CONCAT(YEAR(d),'-',LEFT(MONTHNAME(d),3))
FROM (
    SELECT DATE_ADD('2017-10-01', INTERVAL seq DAY) AS d
    FROM (
        SELECT @row := @row + 1 AS seq
        FROM information_schema.columns,
             (SELECT @row := -1) r
        LIMIT 1200
    ) AS seq_table
) dates
WHERE YEAR(d) BETWEEN 2017 AND 2020
ON DUPLICATE KEY UPDATE date=date;

-- ── Transactions table ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS transactions (
    product_code   VARCHAR(10),
    customer_code  VARCHAR(10),
    market_code    VARCHAR(10),
    order_date     DATE,
    sales_qty      INT,
    sales_amount   DECIMAL(12,2),
    currency       VARCHAR(10),
    profit_margin_percentage DECIMAL(5,2),
    profit_margin  DECIMAL(12,2),
    cost_price     DECIMAL(12,2),
    FOREIGN KEY (product_code)  REFERENCES products(product_code),
    FOREIGN KEY (customer_code) REFERENCES customers(customer_code),
    FOREIGN KEY (market_code)   REFERENCES markets(markets_code)
);

-- Generate realistic transactions using stored procedure
DROP PROCEDURE IF EXISTS generate_transactions;
DELIMITER $$
CREATE PROCEDURE generate_transactions()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE v_date DATE;
    DECLARE v_prod VARCHAR(10);
    DECLARE v_cust VARCHAR(10);
    DECLARE v_mkt  VARCHAR(10);
    DECLARE v_qty  INT;
    DECLARE v_amount DECIMAL(12,2);
    DECLARE v_currency VARCHAR(10);
    DECLARE v_margin_pct DECIMAL(5,2);
    DECLARE v_margin DECIMAL(12,2);
    DECLARE v_cost DECIMAL(12,2);

    WHILE i < 150000 DO
        -- Random date 2018-2020
        SET v_date = DATE_ADD('2017-10-01',
            INTERVAL FLOOR(RAND()*850) DAY);
        -- Random product
        SET v_prod = CONCAT('Prod', LPAD(FLOOR(1+RAND()*17),3,'0'));
        -- Random customer
        SET v_cust = CONCAT('Cus', LPAD(FLOOR(1+RAND()*19),3,'0'));
        -- Random market (India only mostly)
        IF RAND() < 0.97 THEN
            SET v_mkt = CONCAT('Mark', LPAD(FLOOR(1+RAND()*15),3,'0'));
        ELSE
            SET v_mkt = IF(RAND()<0.5,'Mark097','Mark098');
        END IF;

        -- Qty and amounts
        SET v_qty    = FLOOR(1 + RAND()*500);
        SET v_amount = ROUND((50 + RAND()*2000) * v_qty, 2);

        -- Currency (some USD for international)
        IF v_mkt IN ('Mark097','Mark098') THEN
            SET v_currency = 'USD';
            SET v_amount   = ROUND(v_amount / 75, 2);
        ELSE
            SET v_currency = 'INR';
        END IF;

        -- Margin
        SET v_margin_pct = ROUND(-10 + RAND()*30, 2);
        SET v_margin     = ROUND(v_amount * v_margin_pct / 100, 2);
        SET v_cost       = ROUND(v_amount - v_margin, 2);

        INSERT INTO transactions VALUES
        (v_prod, v_cust, v_mkt, v_date,
         v_qty, v_amount, v_currency,
         v_margin_pct, v_margin, v_cost);

        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

CALL generate_transactions();

-- ── Normalise USD → INR ──────────────────────────────────────
UPDATE transactions
SET sales_amount = ROUND(sales_amount * 75, 2),
    profit_margin = ROUND(profit_margin * 75, 2),
    cost_price    = ROUND(cost_price   * 75, 2)
WHERE currency = 'USD';

UPDATE transactions
SET currency = 'INR'
WHERE currency = 'USD';

-- Remove invalid / zero rows
DELETE FROM transactions WHERE sales_amount <= 0;

SELECT CONCAT('✅ Transactions inserted: ', COUNT(*)) AS result FROM transactions;
