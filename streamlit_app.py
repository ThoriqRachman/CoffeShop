import streamlit as st
import pandas as pd
import altair as alt

st.title("Coffee Shop Dashboard")

df = pd.read_excel("Coffe Shop.xlsx")

#Filter Cabang
cabang = st.multiselect(
    "Pilih Store Location",
    options=df["Store Location"].unique(),
    default=df["Store Location"].unique()
)

df = df[df["Store Location"].isin(cabang)]

#Filter Bulan
df["Month"] = pd.to_datetime(df["Transaction Date"]).dt.strftime("%B")

bulan = st.multiselect(
    "Pilih Store Location",
    options=df["Month"].unique(),
    default=df["Month"].unique()
)

df = df[df["Month"].isin(bulan)]

#KPI
col1, col2 = st.columns(2)
with col1:
    avg_qty = round(df["Quantity Sold"].mean(), 2)
    st.metric("Average of Quantity Sold", avg_qty)
with col2:
    total_revenue = round(df["Total Revenue"].sum(), 2)
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

#Transaksi Mingguan
st.subheader("Transaksi Mingguan")
weekly = df.groupby("Day of Week")["Transaction ID"].count().reset_index()
chart_weekly = alt.Chart(weekly).mark_bar().encode(
    x="Day of Week",
    y="Transaction ID"
)
st.altair_chart(chart_weekly, use_container_width=True)

# Penjualan per Produk
st.subheader("Penjualan per Produk")
product_sales = df.groupby("Product Category")["Total Revenue"].sum().reset_index()
chart_pie = alt.Chart(product_sales).mark_arc().encode(
    theta="Total Revenue",
    color="Product Category"
)
st.altair_chart(chart_pie, use_container_width=True)

#Transaksi Perjam
st.subheader("Transaksi Per Jam")
hourly = df.groupby("Hour")["Transaction ID"].count().reset_index()
chart_hourly = alt.Chart(hourly).mark_bar().encode(
    x="Hour",
    y="Transaction ID"
)
st.altair_chart(chart_hourly, use_container_width=True)

#Revenue per Bulan dan Lokasi
st.subheader("Total Revenue per Month dan Store Location")
df["Month"] = pd.to_datetime(df["Transaction Date"]).dt.strftime("%B")
monthly = df.groupby(["Month", "Store Location"])["Total Revenue"].sum().reset_index()
chart_line = alt.Chart(monthly).mark_line(point=True).encode(
    x="Month",
    y="Total Revenue",
    color="Store Location"
)
st.altair_chart(chart_line, use_container_width=True)
