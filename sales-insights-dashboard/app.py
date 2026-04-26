"""
Sales Insights Dashboard — AtliQ Hardware Company
Inspired by Codebasics Data Analysis Project
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Insights | AtliQ Hardware",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 18px 20px;
        border-left: 5px solid #1a3c6e;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .kpi-val  { font-size:1.9rem; font-weight:800; color:#1a3c6e; margin:0; }
    .kpi-lbl  { font-size:0.78rem; color:#888; text-transform:uppercase;
                letter-spacing:.5px; margin:0; }
    .kpi-sub  { font-size:0.82rem; color:#27ae60; font-weight:600; margin:2px 0 0; }
    .kpi-neg  { color:#e74c3c !important; }
    .sec-hdr  { font-size:1rem; font-weight:700; color:#1a3c6e;
                border-bottom:2px solid #e8eaf6; padding-bottom:5px; margin-bottom:8px; }
    .stDownloadButton>button { width:100%; }
</style>
""", unsafe_allow_html=True)

PALETTE = ["#1a3c6e","#2980b9","#27ae60","#f39c12",
           "#e74c3c","#8e44ad","#16a085","#d35400",
           "#2c3e50","#7f8c8d"]


# ── Load data ──────────────────────────────────────────────────
@st.cache_data
def load():
    path = "data/sales_data.csv"
    if not os.path.exists(path):
        st.error("Run `python generate_data.py` first!")
        st.stop()
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df

df_all = load()


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 AtliQ Hardware")
    st.caption("Sales Insights Dashboard")
    st.markdown("---")
    st.markdown("### Filters")

    years = ["All"] + sorted(df_all["year"].unique(), reverse=True)
    sel_yr = st.selectbox("📅 Year", years)

    quarters = ["All","Q1","Q2","Q3","Q4"]
    sel_q = st.selectbox("📆 Quarter", quarters)

    zones = ["All"] + sorted(df_all["zone"].dropna().unique())
    sel_zone = st.selectbox("🗺️ Zone", zones)

    markets = ["All"] + sorted(df_all["market_name"].unique())
    sel_mkt = st.selectbox("🏙️ Market", markets)

    cust_types = ["All","Brick & Mortar","E-Commerce"]
    sel_ctype = st.selectbox("🏪 Customer Type", cust_types)

    prod_types = ["All","Own Brand","Distribution"]
    sel_ptype = st.selectbox("📦 Product Type", prod_types)

    st.markdown("---")
    st.markdown("**🔗 Project Info**")
    st.caption("Inspired by Codebasics Sales Insights Project")
    st.caption("Built by **Rose Sharma** · CSE AI · Rungta College")


# ── Filter ─────────────────────────────────────────────────────
df = df_all.copy()
if sel_yr    != "All": df = df[df["year"]          == int(sel_yr)]
if sel_q     != "All": df = df[df["quarter"]       == sel_q]
if sel_zone  != "All": df = df[df["zone"]          == sel_zone]
if sel_mkt   != "All": df = df[df["market_name"]   == sel_mkt]
if sel_ctype != "All": df = df[df["customer_type"] == sel_ctype]
if sel_ptype != "All": df = df[df["product_type"]  == sel_ptype]

if df.empty:
    st.warning("No data for selected filters. Please adjust.")
    st.stop()


# ── KPIs ───────────────────────────────────────────────────────
rev      = df["sales_amount"].sum()
profit   = df["profit_margin"].sum()
orders   = len(df)
qty      = df["sales_qty"].sum()
margin   = df["profit_margin_percentage"].mean()
avg_sale = rev / orders if orders else 0


def kpi_card(col, label, value, sub=None, neg=False):
    sub_html = ""
    if sub:
        cls = "kpi-neg" if neg else "kpi-sub"
        sub_html = f'<p class="{cls}">{sub}</p>'
    col.markdown(f"""
    <div class="kpi-card">
      <p class="kpi-lbl">{label}</p>
      <p class="kpi-val">{value}</p>
      {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:0.5rem 0 1rem'>
  <h1 style='color:#1a3c6e;font-size:2rem;font-weight:800;margin:0'>
    📊 Sales Insights — AtliQ Hardware
  </h1>
  <p style='color:#888;margin:4px 0'>
    Computer Hardware Business · Data Analysis Project
  </p>
</div>
""", unsafe_allow_html=True)

# Active filters bar
active = [f for f, v in {
    "Year": sel_yr, "Quarter": sel_q, "Zone": sel_zone,
    "Market": sel_mkt, "Customer": sel_ctype, "Product": sel_ptype
}.items() if v != "All"]
if active:
    st.info("🔽 Filters: " + " · ".join(
        f"**{f}**: {v}" for f, v in zip(active, [
            sel_yr, sel_q, sel_zone, sel_mkt, sel_ctype, sel_ptype
        ]) if v != "All"
    ))

# KPI row
c1,c2,c3,c4,c5,c6 = st.columns(6)
kpi_card(c1, "Total Revenue",    f"₹{rev/1e7:.2f} Cr")
kpi_card(c2, "Total Profit",     f"₹{profit/1e7:.2f} Cr",
         neg=(profit < 0))
kpi_card(c3, "Total Orders",     f"{orders:,}")
kpi_card(c4, "Sales Quantity",   f"{qty:,}")
kpi_card(c5, "Avg Profit Margin",f"{margin:.1f}%",
         neg=(margin < 0))
kpi_card(c6, "Avg Order Value",  f"₹{avg_sale:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)


# ── Row 1: Revenue trend + Zone donut ──────────────────────────
r1c1, r1c2 = st.columns([2.2, 1])

with r1c1:
    st.markdown('<p class="sec-hdr">📈 Revenue & Profit Trend (Monthly)</p>',
                unsafe_allow_html=True)
    monthly = (df.groupby(["year","month_num","month_name"])
               .agg(Revenue=("sales_amount","sum"),
                    Profit=("profit_margin","sum"))
               .reset_index()
               .sort_values(["year","month_num"]))
    monthly["Period"] = (monthly["month_name"].str[:3]
                         + " " + monthly["year"].astype(str))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=monthly["Period"], y=monthly["Revenue"],
        name="Revenue", marker_color="#1a3c6e", opacity=0.82
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly["Period"], y=monthly["Profit"],
        name="Profit", mode="lines+markers",
        line=dict(color="#27ae60", width=2.5),
        marker=dict(size=5)
    ), secondary_y=True)
    fig.update_layout(
        height=310, margin=dict(t=10,b=30,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.28),
        hovermode="x unified",
        xaxis=dict(tickangle=-30, tickfont=dict(size=10))
    )
    fig.update_yaxes(tickformat="₹,.0f", gridcolor="#f0f0f0",
                     secondary_y=False)
    fig.update_yaxes(tickformat="₹,.0f", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.markdown('<p class="sec-hdr">🗺️ Revenue by Zone</p>',
                unsafe_allow_html=True)
    zone_df = df.groupby("zone")["sales_amount"].sum().reset_index()
    fig2 = px.pie(zone_df, values="sales_amount", names="zone",
                  color_discrete_sequence=PALETTE, hole=0.45)
    fig2.update_traces(textinfo="percent+label", textfont_size=11,
                       textposition="inside")
    fig2.update_layout(height=310, margin=dict(t=10,b=10,l=10,r=10),
                       showlegend=False, paper_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)


# ── Row 2: Top customers + Top markets ────────────────────────
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown('<p class="sec-hdr">🏆 Top 5 Customers by Revenue</p>',
                unsafe_allow_html=True)
    top_cust = (df.groupby(["customer_name","customer_type"])
                .agg(Revenue=("sales_amount","sum"),
                     Profit=("profit_margin","sum"))
                .reset_index()
                .sort_values("Revenue", ascending=False)
                .head(5))
    fig3 = px.bar(
        top_cust.sort_values("Revenue"),
        x="Revenue", y="customer_name", orientation="h",
        color="customer_type",
        color_discrete_map={"Brick & Mortar":"#1a3c6e",
                            "E-Commerce":"#2980b9"},
        text=top_cust.sort_values("Revenue")["Revenue"]
             .apply(lambda x: f"₹{x/1e6:.1f}M")
    )
    fig3.update_traces(textposition="outside")
    fig3.update_layout(
        height=280, margin=dict(t=10,b=10,l=10,r=80),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis_title="", xaxis=dict(tickformat="₹,.0f",
                                   gridcolor="#f0f0f0"),
        legend=dict(title="", orientation="h", y=-0.25)
    )
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.markdown('<p class="sec-hdr">🏙️ Top 5 Markets by Revenue</p>',
                unsafe_allow_html=True)
    top_mkt = (df.groupby(["market_name","zone"])
               .agg(Revenue=("sales_amount","sum"),
                    Profit=("profit_margin","sum"))
               .reset_index()
               .sort_values("Revenue", ascending=False)
               .head(5))
    fig4 = px.bar(
        top_mkt.sort_values("Revenue"),
        x="Revenue", y="market_name", orientation="h",
        color="zone",
        color_discrete_sequence=PALETTE,
        text=top_mkt.sort_values("Revenue")["Revenue"]
             .apply(lambda x: f"₹{x/1e6:.1f}M")
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(
        height=280, margin=dict(t=10,b=10,l=10,r=80),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis_title="", xaxis=dict(tickformat="₹,.0f",
                                   gridcolor="#f0f0f0"),
        legend=dict(title="Zone", orientation="h", y=-0.25)
    )
    st.plotly_chart(fig4, use_container_width=True)


# ── Row 3: Profit margin analysis ─────────────────────────────
r3c1, r3c2, r3c3 = st.columns(3)

with r3c1:
    st.markdown('<p class="sec-hdr">💰 Profit Margin % by Market</p>',
                unsafe_allow_html=True)
    mkt_margin = (df.groupby("market_name")
                  .agg(Margin=("profit_margin_percentage","mean"),
                       Revenue=("sales_amount","sum"))
                  .reset_index()
                  .sort_values("Margin", ascending=False))
    fig5 = px.bar(
        mkt_margin, x="market_name", y="Margin",
        color="Margin",
        color_continuous_scale=["#e74c3c","#f39c12","#27ae60"],
        text=mkt_margin["Margin"].apply(lambda x: f"{x:.1f}%")
    )
    fig5.update_traces(textposition="outside")
    fig5.update_layout(
        height=280, margin=dict(t=10,b=40,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickangle=-30, title=""),
        yaxis=dict(title="Margin %", gridcolor="#f0f0f0"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig5, use_container_width=True)

with r3c2:
    st.markdown('<p class="sec-hdr">📦 Own Brand vs Distribution</p>',
                unsafe_allow_html=True)
    prod_type_df = (df.groupby("product_type")
                    .agg(Revenue=("sales_amount","sum"),
                         Profit=("profit_margin","sum"),
                         Margin=("profit_margin_percentage","mean"))
                    .reset_index())
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        x=prod_type_df["product_type"],
        y=prod_type_df["Revenue"],
        name="Revenue", marker_color="#1a3c6e", opacity=0.85
    ))
    fig6.add_trace(go.Bar(
        x=prod_type_df["product_type"],
        y=prod_type_df["Profit"],
        name="Profit", marker_color="#27ae60", opacity=0.85
    ))
    fig6.update_layout(
        height=280, barmode="group",
        margin=dict(t=10,b=10,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=-0.2),
        yaxis=dict(tickformat="₹,.0f", gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig6, use_container_width=True)

with r3c3:
    st.markdown('<p class="sec-hdr">🏪 Brick & Mortar vs E-Commerce</p>',
                unsafe_allow_html=True)
    ctype_df = (df.groupby("customer_type")
                .agg(Revenue=("sales_amount","sum"),
                     Orders=("sales_amount","count"))
                .reset_index())
    fig7 = px.pie(
        ctype_df, values="Revenue", names="customer_type",
        color_discrete_map={"Brick & Mortar":"#1a3c6e",
                            "E-Commerce":"#2980b9"},
        hole=0.45
    )
    fig7.update_traces(textinfo="percent+label",
                       textfont_size=12, textposition="inside")
    fig7.update_layout(
        height=280, margin=dict(t=10,b=10,l=10,r=10),
        showlegend=False, paper_bgcolor="white"
    )
    st.plotly_chart(fig7, use_container_width=True)


# ── Row 4: Quarterly + Revenue vs Profit scatter ───────────────
r4c1, r4c2 = st.columns([1.3, 1])

with r4c1:
    st.markdown('<p class="sec-hdr">📆 Quarterly Revenue Trend</p>',
                unsafe_allow_html=True)
    qtr = (df.groupby(["year","quarter"])
           .agg(Revenue=("sales_amount","sum"),
                Profit=("profit_margin","sum"))
           .reset_index()
           .sort_values(["year","quarter"]))
    qtr["Label"] = qtr["quarter"] + " " + qtr["year"].astype(str)

    fig8 = px.line(
        qtr, x="Label", y=["Revenue","Profit"],
        markers=True,
        color_discrete_map={"Revenue":"#1a3c6e","Profit":"#27ae60"}
    )
    fig8.update_traces(line_width=2.5, marker_size=7)
    fig8.update_layout(
        height=280, margin=dict(t=10,b=30,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickangle=-20, title=""),
        yaxis=dict(tickformat="₹,.0f", gridcolor="#f0f0f0"),
        legend=dict(title="", orientation="h", y=-0.3)
    )
    st.plotly_chart(fig8, use_container_width=True)

with r4c2:
    st.markdown('<p class="sec-hdr">🔵 Revenue vs Profit by Market</p>',
                unsafe_allow_html=True)
    bubble = (df.groupby("market_name")
              .agg(Revenue=("sales_amount","sum"),
                   Profit=("profit_margin","sum"),
                   Qty=("sales_qty","sum"))
              .reset_index())
    fig9 = px.scatter(
        bubble, x="Revenue", y="Profit",
        size="Qty", color="market_name",
        color_discrete_sequence=PALETTE,
        hover_name="market_name",
        size_max=40
    )
    fig9.update_layout(
        height=280, margin=dict(t=10,b=10,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickformat="₹,.0f", gridcolor="#f0f0f0",
                   title="Revenue"),
        yaxis=dict(tickformat="₹,.0f", gridcolor="#f0f0f0",
                   title="Profit"),
        showlegend=False
    )
    st.plotly_chart(fig9, use_container_width=True)


# ── Row 5: Summary table ───────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="sec-hdr">📋 Market-wise Summary Table</p>',
            unsafe_allow_html=True)

summary = (df.groupby(["market_name","zone"])
           .agg(
               Revenue=("sales_amount","sum"),
               Profit=("profit_margin","sum"),
               Orders=("sales_amount","count"),
               Qty=("sales_qty","sum"),
               Avg_Margin=("profit_margin_percentage","mean")
           )
           .reset_index()
           .sort_values("Revenue", ascending=False))

summary["Revenue"]    = summary["Revenue"].apply(lambda x: f"₹{x/1e6:.2f}M")
summary["Profit"]     = summary["Profit"].apply(lambda x: f"₹{x/1e6:.2f}M")
summary["Avg_Margin"] = summary["Avg_Margin"].apply(lambda x: f"{x:.1f}%")
summary["Qty"]        = summary["Qty"].apply(lambda x: f"{x:,}")
summary["Orders"]     = summary["Orders"].apply(lambda x: f"{x:,}")
summary.columns = ["Market","Zone","Revenue","Profit",
                   "Orders","Qty Sold","Avg Margin"]

st.dataframe(summary, use_container_width=True, height=320)


# ── Row 6: Transactions table ──────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="sec-hdr">📑 Transaction Records</p>',
            unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns([2,1,3])
with sc1:
    search = st.text_input("🔍 Search customer / market", "")
with sc2:
    n = st.selectbox("Show", [10,25,50,100], index=0)

disp = df[[
    "order_date","customer_name","customer_type",
    "market_name","zone","product_code","product_type",
    "sales_qty","sales_amount","profit_margin",
    "profit_margin_percentage","currency"
]].copy()

disp.columns = [
    "Date","Customer","Type","Market","Zone",
    "Product","Prod Type","Qty","Revenue (₹)",
    "Profit (₹)","Margin %","Currency"
]

if search:
    mask = (
        disp["Customer"].str.contains(search, case=False, na=False) |
        disp["Market"].str.contains(search, case=False, na=False)
    )
    disp = disp[mask]

disp = disp.sort_values("Revenue (₹)", ascending=False).head(n)
disp["Revenue (₹)"] = disp["Revenue (₹)"].apply(lambda x: f"₹{x:,.0f}")
disp["Profit (₹)"]  = disp["Profit (₹)"].apply(lambda x: f"₹{x:,.0f}")
disp["Margin %"]     = disp["Margin %"].apply(lambda x: f"{x:.1f}%")

st.dataframe(disp, use_container_width=True, height=320)

# Download
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Full Dataset (CSV)",
    data=csv,
    file_name="atliq_sales_data.csv",
    mime="text/csv"
)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#aaa;font-size:0.8rem;padding:1rem 0'>
    📊 Sales Insights Dashboard · AtliQ Hardware ·
    Inspired by Codebasics · Built by <strong>Rose Sharma</strong> ·
    Python · Pandas · Plotly · Streamlit
</div>
""", unsafe_allow_html=True)
