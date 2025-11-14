import streamlit as st
import pandas as pd
import altair as alt

# Page Config
st.set_page_config(page_title="Coffee Shop Dashboard", layout="wide")

# --- HEADER ---
st.markdown("""
# ☕ Coffee Shop Dashboard
# """)

# Load Data
df = pd.read_excel("Coffe Shop.xlsx")

# Month Mapping
df["Month_Num"] = pd.to_datetime(df["Transaction Date"]).dt.month
month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

# --- FILTER SECTION ---
st.sidebar.markdown("### 🔧 Filters Panel")("Filters")

# Store Filter
store_filter = st.sidebar.multiselect(
    "Select Store Location",
    options=df["Store Location"].unique(),
    default=df["Store Location"].unique()
)
df = df[df["Store Location"].isin(store_filter)]

st.sidebar.markdown("---")
# Month Slider
min_month = int(df["Month_Num"].min())
max_month = int(df["Month_Num"].max())

selected_month = st.sidebar.slider(
    "Select Month Range",
    min_value=min_month,
    max_value=max_month,
    value=(min_month, max_month)
)

df = df[(df["Month_Num"] >= selected_month[0]) & (df["Month_Num"] <= selected_month[1])]
df["Month"] = df["Month_Num"].map(month_map)

# ---------- KPI ROW ----------
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_qty = round(df["Quantity Sold"].mean(), 2)
    st.metric("Average Quantity Sold", avg_qty)

with col2:
    total_revenue = df["Total Revenue"].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col3:
    total_trans = df["Transaction ID"].nunique()
    st.metric("Total Transactions", total_trans)

with col4:
    avg_rev = df["Total Revenue"].mean()
    st.metric("Avg Revenue / Transaction", f"${avg_rev:,.2f}")

# ---------- 2nd ROW: GRAPHS ----------
st.markdown("## 📈 Sales Performance Insights")
col4, col5, col6 = st.columns(3)

# Weekly Transactions
with col4:
    st.subheader("Weekly Transactions")
    weekly = df.groupby("Day of Week")["Transaction ID"].count().reset_index()
    chart_weekly = alt.Chart(weekly).mark_bar().encode(
        x=alt.X("Day of Week", sort=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]),
        y="Transaction ID"
    )
    st.altair_chart(chart_weekly, use_container_width=True)

# Product Sales Pie
with col5:
    st.subheader("Revenue by Product Category")
    product_sales = df.groupby("Product Category")["Total Revenue"].sum().reset_index()
    chart_pie = alt.Chart(product_sales).mark_arc().encode(
        theta="Total Revenue",
        color="Product Category"
    )
    st.altair_chart(chart_pie, use_container_width=True)

# Hourly Transactions
with col6:
    st.subheader("Hourly Transactions")
    hourly = df.groupby("Hour")["Transaction ID"].count().reset_index()
    chart_hourly = alt.Chart(hourly).mark_bar().encode(
        x="Hour",
        y="Transaction ID"
    )
    st.altair_chart(chart_hourly, use_container_width=True)

# ---------- 3rd ROW ----------
st.markdown("## 📅 Monthly Revenue Breakdown")
col7, col8, col9 = st.columns(3)

# Revenue by Month & Location
with col7:
    st.subheader("Monthly Revenue by Store")
    monthly = df.groupby(["Month", "Store Location"])["Total Revenue"].sum().reset_index()
    chart_line = alt.Chart(monthly).mark_line(point=True).encode(
        x="Month",
        y="Total Revenue",
        color="Store Location"
    )
    st.altair_chart(chart_line, use_container_width=True)

# Top Products
with col8:
    st.subheader("Top Products by Revenue")
    top_product = df.groupby("Product Category")["Total Revenue"].sum().reset_index().sort_values(by="Total Revenue", ascending=False).head(5)
    chart_top = alt.Chart(top_product).mark_bar().encode(
        x="Product Category",
        y="Total Revenue"
    )
    st.altair_chart(chart_top, use_container_width=True)

# Avg Revenue Summary
with col9:
    st.subheader("Average Revenue per Transaction")
    avg_rev = df["Total Revenue"].mean()
    st.metric("Avg Revenue / Transaction", f"${avg_rev:,.2f}")

