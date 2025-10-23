import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Trading212 Advanced Analytics", layout="wide")

st.title("Trading212 Advanced Portfolio Analytics")
st.markdown("*Interactive dashboard for analyzing your trading history and portfolio performance*")

# Sample data
orders_data = {
    "items": [
        {"type": "MARKET", "id": 40610332676, "ticker": "ENB_US_EQ", "filledQuantity": 0.19728365, "orderedValue": 8.01, "filledValue": 8.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 47.24, "fillCost": 8, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332647, "ticker": "NFLX_US_EQ", "filledQuantity": 0.00190361, "orderedValue": 2, "filledValue": 2, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 1223.9, "fillCost": 2, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332638, "ticker": "VICI_US_EQ", "filledQuantity": 0.29898492, "orderedValue": 8.01, "filledValue": 8.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 31.17, "fillCost": 8, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332633, "ticker": "SPG_US_EQ", "filledQuantity": 0.05202277, "orderedValue": 8.01, "filledValue": 8.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 179.14, "fillCost": 8, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332610, "ticker": "ADC_US_EQ", "filledQuantity": 0.15422277, "orderedValue": 10.01, "filledValue": 10.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 75.46, "fillCost": 9.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332599, "ticker": "FB_US_EQ", "filledQuantity": 0.00957515, "orderedValue": 6, "filledValue": 6, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 728.76, "fillCost": 5.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332574, "ticker": "TFC_US_EQ", "filledQuantity": 0.2711475, "orderedValue": 10.01, "filledValue": 10.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 42.92, "fillCost": 9.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332569, "ticker": "NEE_US_EQ", "filledQuantity": 0.16511869, "orderedValue": 12.01, "filledValue": 12.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 84.59, "fillCost": 11.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332564, "ticker": "WMT_US_EQ", "filledQuantity": 0.02171939, "orderedValue": 2, "filledValue": 2, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 107.27, "fillCost": 2, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332558, "ticker": "RHMd_EQ", "filledQuantity": 0.00682774, "orderedValue": 12.01, "filledValue": 12.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 1759, "fillCost": 12.01, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332549, "ticker": "O_US_EQ", "filledQuantity": 0.23152048, "orderedValue": 12.01, "filledValue": 12.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 60.33, "fillCost": 11.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332540, "ticker": "AMZN_US_EQ", "filledQuantity": 0.10864443, "orderedValue": 20.03, "filledValue": 20.03, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 214.45, "fillCost": 20, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332531, "ticker": "VUAGl_EQ", "filledQuantity": 0.14486842, "orderedValue": 16.02, "filledValue": 16.02, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 95.99, "fillCost": 16, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332526, "ticker": "NVDA_US_EQ", "filledQuantity": 0.14003977, "orderedValue": 22.03, "filledValue": 22.03, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 183.01, "fillCost": 22, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332521, "ticker": "ASML_US_EQ", "filledQuantity": 0.0067398, "orderedValue": 6, "filledValue": 6, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 1035.34, "fillCost": 5.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332512, "ticker": "AAPL_US_EQ", "filledQuantity": 0.0629322, "orderedValue": 14.02, "filledValue": 14.02, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 259.15, "fillCost": 14, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332507, "ticker": "GOOG_US_EQ", "filledQuantity": 0.04560883, "orderedValue": 10.01, "filledValue": 10.01, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 255.16, "fillCost": 9.99, "status": "FILLED"},
        {"type": "MARKET", "id": 40610332502, "ticker": "MSFT_US_EQ", "filledQuantity": 0.04980709, "orderedValue": 22.03, "filledValue": 22.03, "executor": "AUTOINVEST", "dateCreated": "2025-10-20T13:58:19.000Z", "fillPrice": 514.55, "fillCost": 22, "status": "FILLED"},
        {"type": "MARKET", "id": 18450606708, "ticker": "ADC_US_EQ", "orderedValue": 5, "filledValue": 0, "executor": "AUTOINVEST", "dateCreated": "2024-08-03T17:08:24.000Z", "status": "CANCELLED"},
        {"type": "MARKET", "id": 18450606706, "ticker": "TFC_US_EQ", "orderedValue": 5, "filledValue": 0, "executor": "AUTOINVEST", "dateCreated": "2024-08-03T17:08:24.000Z", "status": "CANCELLED"},
    ]
}

# Data processing
df = pd.DataFrame(orders_data["items"])
df["dateCreated"] = pd.to_datetime(df["dateCreated"])
df["ticker"] = df["ticker"].str.replace("_US_EQ", "").str.replace("_EQ", "")
df["cost"] = df.get("fillCost", df.get("orderedValue", 0)).fillna(0)
df["quantity"] = df.get("filledQuantity", 0).fillna(0)
df["fillPrice"] = df.get("fillPrice", 0).fillna(0)
df["avg_price_per_share"] = (df["cost"] / df["quantity"]).replace([np.inf, -np.inf], 0).fillna(0)

df_filled = df[df["status"] == "FILLED"].copy()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Date range",
        value=(df["dateCreated"].min().date(), df["dateCreated"].max().date()),
    )
    selected_tickers = st.multiselect(
        "Tickers",
        sorted(df_filled["ticker"].unique()),
        default=sorted(df_filled["ticker"].unique())[:5]
    )

df_filtered = df_filled[
    (df_filled["dateCreated"].dt.date >= date_range[0]) &
    (df_filled["dateCreated"].dt.date <= date_range[1]) &
    (df_filled["ticker"].isin(selected_tickers))
].copy()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Dashboard", "Holdings", "Trading Patterns", 
    "Stock Analysis", "Performance", "Raw Data"
])

with tab1:
    st.subheader("Portfolio Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Trades", len(df_filtered))
    col2.metric("Total Invested", f"${df_filtered['cost'].sum():.2f}")
    col3.metric("Unique Stocks", df_filtered["ticker"].nunique())
    col4.metric("Avg Trade", f"${df_filtered['cost'].mean():.2f}")
    col5.metric("Cancelled", len(df[df["status"] == "CANCELLED"]))
    
    st.divider()
    
    cum_data = df_filtered.sort_values("dateCreated").copy()
    cum_data["cumulative"] = cum_data["cost"].cumsum()
    fig = px.area(cum_data, x="dateCreated", y="cumulative",
                  title="Cumulative Investment", 
                  labels={"dateCreated": "Date", "cumulative": "Total ($)"})
    st.plotly_chart(fig, use_container_width=True)
    
    heatmap_data = df_filtered.copy()
    fig = px.density_heatmap(heatmap_data, x="dateCreated", y="ticker",
                             title="Trading Activity Heatmap")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Current Holdings")
    holdings = df_filtered.groupby("ticker").agg({
        "quantity": "sum",
        "cost": "sum",
        "fillPrice": "mean",
        "id": "count",
    }).reset_index()
    holdings.columns = ["Ticker", "Total Shares", "Total Cost", "Avg Price", "Trades"]
    holdings = holdings.sort_values("Total Cost", ascending=False)
    holdings["% Portfolio"] = (holdings["Total Cost"] / holdings["Total Cost"].sum() * 100).round(2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(holdings, use_container_width=True, hide_index=True)
    with col2:
        fig = px.pie(holdings, names="Ticker", values="Total Cost", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(holdings.nlargest(10, "Total Cost"), x="Ticker", y="Total Cost",
                 color="% Portfolio", color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Trading Behavior")
    col1, col2 = st.columns(2)
    
    with col1:
        trades_per_day = df_filtered.groupby(df_filtered["dateCreated"].dt.date).size()
        fig = px.bar(x=trades_per_day.index, y=trades_per_day.values,
                     title="Daily Trades", labels={"x": "Date", "y": "Trades"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        inv_per_day = df_filtered.groupby(df_filtered["dateCreated"].dt.date)["cost"].sum()
        fig = px.bar(x=inv_per_day.index, y=inv_per_day.values,
                     title="Daily Investment", labels={"x": "Date", "y": "Amount ($)"})
        st.plotly_chart(fig, use_container_width=True)
    
    df_filtered["hour"] = df_filtered["dateCreated"].dt.hour
    by_hour = df_filtered.groupby("hour").agg({"id": "count", "cost": "sum"}).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=by_hour["hour"], y=by_hour["id"], name="Trades"), secondary_y=False)
    fig.add_trace(go.Scatter(x=by_hour["hour"], y=by_hour["cost"], name="Investment", mode="lines+markers"), secondary_y=True)
    fig.update_layout(title="Activity by Hour")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Stock Analysis")
    selected_stock = st.selectbox("Select stock", sorted(df_filtered["ticker"].unique()))
    stock_data = df_filtered[df_filtered["ticker"] == selected_stock]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trades", len(stock_data))
    col2.metric("Invested", f"${stock_data['cost'].sum():.2f}")
    col3.metric("Shares", f"{stock_data['quantity'].sum():.4f}")
    col4.metric("Avg Price", f"${stock_data['avg_price_per_share'].mean():.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        stock_sorted = stock_data.sort_values("dateCreated")
        fig = px.line(stock_sorted, x="dateCreated", y="fillPrice", markers=True,
                      title=f"{selected_stock} Price Trend")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        stock_sorted["cum"] = stock_sorted["cost"].cumsum()
        fig = px.line(stock_sorted, x="dateCreated", y="cum", markers=True,
                      title=f"{selected_stock} Cumulative Investment")
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trades/Day", f"{len(df_filtered) / max(1, (df_filtered['dateCreated'].max() - df_filtered['dateCreated'].min()).days + 1):.1f}")
    col2.metric("Success Rate", "100%")
    col3.metric("Trade Variance", f"${df_filtered['cost'].std():.2f}")
    col4.metric("Largest Trade", f"${df_filtered['cost'].max():.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df_filtered, x="cost", nbins=20, title="Trade Size Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df_filtered[df_filtered["quantity"] > 0], x="quantity", nbins=20, title="Shares Distribution")
        st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.subheader("Transaction Data")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download CSV"):
            st.download_button("CSV", df_filtered.to_csv(index=False), "data.csv", "text/csv")
    with col2:
        if st.button("Download JSON"):
            st.download_button("JSON", df_filtered.to_json(orient="records"), "data.json", "application/json")
    
    st.dataframe(df_filtered[["dateCreated", "ticker", "quantity", "fillPrice", "cost"]].copy(), 
                 use_container_width=True, hide_index=True)
