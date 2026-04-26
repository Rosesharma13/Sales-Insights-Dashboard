# 📊 Sales Insights Dashboard — AtliQ Hardware

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## 📌 Problem Statement

AtliQ Hardware is a computer hardware supplier facing challenges in a dynamically changing market. The Sales Director wants real-time sales insights to make data-driven decisions. This dashboard provides a comprehensive view of revenue, profit margins, regional performance, and customer analytics.

> Inspired by the [Codebasics Sales Insights Data Analysis Project](https://codebasics.io/resources/sales-insights-data-analysis-project)

## ✨ Dashboard Features

- 📈 **Revenue & Profit Trend** — Monthly dual-axis bar + line chart
- 🗺️ **Zone-wise Analysis** — North, South, Central revenue breakdown
- 🏆 **Top 5 Customers** — By revenue with customer type split
- 🏙️ **Top 5 Markets** — Best performing cities
- 💰 **Profit Margin Analysis** — By market, product type
- 📦 **Own Brand vs Distribution** — Product type comparison
- 🏪 **Brick & Mortar vs E-Commerce** — Channel analysis
- 📆 **Quarterly Trend** — Revenue and profit over quarters
- 🔵 **Revenue vs Profit Scatter** — Bubble chart by market
- 📋 **Interactive Data Tables** — Searchable, downloadable
- 🔽 **6 Filter Controls** — Year, Quarter, Zone, Market, Customer Type, Product Type

## 🗄️ Database Schema

```
sales_insights_db
├── transactions   (150,000+ rows)
├── customers      (20 customers)
├── products       (18 products)
├── markets        (17 markets)
└── date           (date dimension)
```

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **MySQL** | Database (AtliQ schema) |
| **Pandas** | Data cleaning & analysis |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Dashboard web app |
| **SQL** | Data extraction & analysis queries |

## 📁 Project Structure

```
sales-insights-dashboard/
├── app.py                 # Streamlit dashboard
├── generate_data.py       # Sample data generator
├── db_dump.sql            # MySQL database schema + data
├── analysis_queries.sql   # SQL analysis queries
├── data/
│   └── sales_data.csv     # Pre-generated dataset
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 How to Run

### Option A — Quick Start (CSV mode, no MySQL needed)

```bash
# Step 1: Clone repository
git clone https://github.com/yourusername/sales-insights-dashboard.git
cd sales-insights-dashboard

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Generate data (already included in data/)
python generate_data.py

# Step 4: Run dashboard
streamlit run app.py
```

Open **http://localhost:8501** 🎉

### Option B — Full MySQL Setup

```bash
# Import database
mysql -u root -p < db_dump.sql

# Run SQL analysis queries
mysql -u root -p sales_insights_db < analysis_queries.sql

# Then run dashboard
streamlit run app.py
```

## 📊 Key SQL Queries Used

```sql
-- Total Revenue
SELECT ROUND(SUM(sales_amount)/10000000, 2) AS total_revenue_cr
FROM transactions;

-- Revenue by Market
SELECT m.markets_name, ROUND(SUM(t.sales_amount)/1000000, 2) AS revenue_mn
FROM transactions t
JOIN markets m ON t.market_code = m.markets_code
GROUP BY m.markets_name
ORDER BY revenue_mn DESC;

-- Profit Margin by Zone
SELECT m.zone, ROUND(AVG(t.profit_margin_percentage), 2) AS avg_margin
FROM transactions t
JOIN markets m ON t.market_code = m.markets_code
GROUP BY m.zone;
```

## 📸 Screenshots

*(Add screenshots of your running dashboard here)*

## 🔑 Key Learnings

- **AIMS Grid** — Project planning using Purpose, Stakeholders, End Result, Success Criteria
- **SQL Analysis** — Joins, aggregations, filtering for business insights
- **Data Cleaning** — Removing invalid currencies, negative values, duplicate entries
- **ETL** — Extract from MySQL, Transform with Pandas, Load into dashboard
- **Business Intelligence** — Translating raw sales data into actionable insights
- **Dashboard Design** — Building executive-level dashboards with Streamlit + Plotly

## 👩‍💻 Author

**Rose Sharma**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rose-sharma13)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white)](mailto:rosesharmaa132003@gmail.com)

## 🙏 Credits

Project concept inspired by [Codebasics](https://codebasics.io) Sales Insights Data Analysis Project.

## 📄 License

MIT License
