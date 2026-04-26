"""
generate_data.py
Generates sales_data.csv matching the Codebasics AtliQ Hardware schema.
Run: python generate_data.py
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

# ── Master data matching db_dump.sql ──────────────────────────
CUSTOMERS = {
    'Cus001': ('Surge Stores',           'Brick & Mortar'),
    'Cus002': ('Nomad Stores',           'Brick & Mortar'),
    'Cus003': ('Excel Stores',           'Brick & Mortar'),
    'Cus004': ('Surface Stores',         'Brick & Mortar'),
    'Cus005': ('Premium Stores',         'Brick & Mortar'),
    'Cus006': ('Nixon',                  'E-Commerce'),
    'Cus007': ('Sage',                   'E-Commerce'),
    'Cus008': ('Electricalsara Stores',  'Brick & Mortar'),
    'Cus009': ('Electricalslytical',     'E-Commerce'),
    'Cus010': ('Electricalsbea Stores',  'Brick & Mortar'),
    'Cus011': ('Info Stores',            'Brick & Mortar'),
    'Cus012': ('Synthetic',              'E-Commerce'),
    'Cus013': ('Path',                   'E-Commerce'),
    'Cus014': ('Logic Stores',           'Brick & Mortar'),
    'Cus015': ('Leader',                 'E-Commerce'),
    'Cus016': ('Propel',                 'E-Commerce'),
    'Cus017': ('Sunset',                 'E-Commerce'),
    'Cus018': ('Control',                'E-Commerce'),
    'Cus019': ('Epic Stores',            'Brick & Mortar'),
    'Cus020': ('Novus',                  'E-Commerce'),
}

PRODUCTS = {
    'Prod001': 'Own Brand',    'Prod002': 'Own Brand',
    'Prod003': 'Own Brand',    'Prod004': 'Own Brand',
    'Prod005': 'Own Brand',    'Prod006': 'Distribution',
    'Prod007': 'Distribution', 'Prod008': 'Distribution',
    'Prod009': 'Own Brand',    'Prod010': 'Distribution',
    'Prod011': 'Own Brand',    'Prod012': 'Distribution',
    'Prod013': 'Own Brand',    'Prod014': 'Distribution',
    'Prod015': 'Own Brand',    'Prod016': 'Distribution',
    'Prod017': 'Own Brand',    'Prod018': 'Distribution',
}

MARKETS = {
    'Mark001': ('Chennai',       'South'),
    'Mark002': ('Mumbai',        'Central'),
    'Mark003': ('Ahmedabad',     'North'),
    'Mark004': ('Delhi NCR',     'North'),
    'Mark005': ('Kanpur',        'North'),
    'Mark006': ('Bengaluru',     'South'),
    'Mark007': ('Bhopal',        'Central'),
    'Mark008': ('Lucknow',       'North'),
    'Mark009': ('Patna',         'Central'),
    'Mark010': ('Surat',         'North'),
    'Mark011': ('Nagpur',        'Central'),
    'Mark012': ('Hyderabad',     'South'),
    'Mark013': ('Bhubaneswar',   'South'),
    'Mark014': ('Kochi',         'South'),
    'Mark015': ('Pune',          'Central'),
}

# ── Generate transactions ──────────────────────────────────────
rows = []
start = datetime(2017, 10, 1)

for _ in range(15000):
    order_date = start + timedelta(days=random.randint(0, 850))
    year       = order_date.year
    month      = order_date.strftime("%B")
    month_num  = order_date.month
    quarter    = f"Q{(month_num-1)//3+1}"

    cust_code  = random.choice(list(CUSTOMERS.keys()))
    cust_name, cust_type = CUSTOMERS[cust_code]

    prod_code  = random.choice(list(PRODUCTS.keys()))
    prod_type  = PRODUCTS[prod_code]

    mkt_code   = random.choice(list(MARKETS.keys()))
    mkt_name, zone = MARKETS[mkt_code]

    # Sales qty — higher for top markets
    base_qty = 50 if mkt_name in ['Delhi NCR','Mumbai','Chennai'] else 30
    sales_qty = max(1, int(np.random.normal(base_qty, base_qty * 0.5)))

    # Revenue — seasonal boost Oct-Dec
    base_price  = random.uniform(50, 2000)
    season_mult = 1.25 if month_num in [10,11,12] else 1.0
    sales_amount = round(base_price * sales_qty * season_mult, 2)

    # Profit margin — own brand higher
    if prod_type == 'Own Brand':
        margin_pct = round(random.uniform(5, 25), 2)
    else:
        margin_pct = round(random.uniform(-5, 15), 2)

    profit_margin = round(sales_amount * margin_pct / 100, 2)
    cost_price    = round(sales_amount - profit_margin, 2)

    rows.append({
        'order_date':               order_date.strftime('%Y-%m-%d'),
        'year':                     year,
        'month_name':               month,
        'month_num':                month_num,
        'quarter':                  quarter,
        'cy_date':                  (order_date.replace(year=order_date.year-1)
                                     .strftime('%Y-%m-%d')),
        'product_code':             prod_code,
        'product_type':             prod_type,
        'customer_code':            cust_code,
        'customer_name':            cust_name,
        'customer_type':            cust_type,
        'market_code':              mkt_code,
        'market_name':              mkt_name,
        'zone':                     zone,
        'sales_qty':                sales_qty,
        'sales_amount':             sales_amount,
        'currency':                 'INR',
        'profit_margin_percentage': margin_pct,
        'profit_margin':            profit_margin,
        'cost_price':               cost_price,
    })

df = pd.DataFrame(rows).sort_values('order_date').reset_index(drop=True)
os.makedirs('data', exist_ok=True)
df.to_csv('data/sales_data.csv', index=False)

print(f"✅ Generated {len(df):,} transactions")
print(f"   Period : {df['order_date'].min()} → {df['order_date'].max()}")
print(f"   Revenue: ₹{df['sales_amount'].sum()/1e7:.2f} Cr")
print(f"   Profit : ₹{df['profit_margin'].sum()/1e7:.2f} Cr")
print("\n▶  Now run:  streamlit run app.py")
