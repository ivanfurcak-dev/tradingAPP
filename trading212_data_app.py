import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Trading212 Portfolio Analysis", layout="wide")

st.title("Trading212 Portfolio Analysis")

# Sample data from your API response
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

# Convert to DataFrame
df = pd.DataFrame(orders_data["items"])

# Clean data
df["dateCreated"] = pd.to_datetime(df["dateCreated"])
df["ticker"] = df["ticker"].str.replace("_US_EQ", "").str.replace("_EQ", "")
df["cost"] = df.get("fillCost", df.get("orderedValue", 0))
df["quantity"] = df.get("filledQuantity", 0)

# Filter only filled orders
df_filled = df[df["status"] == "FILLED"].copy()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Holdings", "Trading Activity", "Raw Data"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trades (Filled)", len(df_filled))
    
    with col2:
        st.metric("Total Invested", f"${df_filled['cost'].sum():.2f}")
    
    with col3:
        st.metric("Unique Stocks", df_filled["ticker"].nunique())
    
    with col4:
        st.metric("Cancelled Orders", len(df[df["status"] == "CANCELLED"]))
    
    st.divider()
    
    # Trading over time
    st.subheader("Trading Activity Over Time")
    daily_trades = df_filled.groupby(df_filled["dateCreated"].dt.date).agg({
        "cost": "sum",
        "id": "count"
    }).reset_index()
    daily_trades.columns = ["Date", "Amount Invested", "Number of Trades"]
    
    fig = px.bar(daily_trades, x="Date", y="Amount Invested", 
                 hover_data=["Number of Trades"],
                 title="Daily Investment Amount",
                 labels={"Amount Invested": "$ Invested"})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Holdings by Stock")
    
    # Holdings summary
    holdings = df_filled.groupby("ticker").agg({
        "quantity": "sum",
        "cost": "sum",
        "fillPrice": "first",
        "id": "count"
    }).reset_index()
    holdings.columns = ["Ticker", "Total Quantity", "Total Cost", "Avg Price", "Trades"]
    holdings = holdings.sort_values("Total Cost", ascending=False)
    holdings["% of Portfolio"] = (holdings["Total Cost"] / holdings["Total Cost"].sum() * 100).round(2)
    
    st.dataframe(holdings, use_container_width=True, hide_index=True)
    
    # Pie chart
    fig = px.pie(holdings, names="Ticker", values="Total Cost", 
                 title="Portfolio Allocation by Investment Amount",
                 hover_data={"Total Cost": ":.2f"})
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Trading Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top stocks by investment
        top_invested = df_filled.nlargest(10, "cost")[["ticker", "cost", "fillPrice", "quantity"]]
        fig = px.bar(top_invested, x="ticker", y="cost", 
                    title="Top 10 Stocks by Investment Amount",
                    labels={"cost": "Amount Invested ($)", "ticker": "Stock"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Number of trades per stock
        trades_per_stock = df_filled["ticker"].value_counts().head(10)
        fig = px.bar(x=trades_per_stock.index, y=trades_per_stock.values,
                    title="Most Traded Stocks",
                    labels={"x": "Stock", "y": "Number of Trades"})
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("All Orders")
    
    # Display options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        filter_status = st.multiselect("Filter by Status", df["status"].unique(), default=df["status"].unique())
    
    with col2:
        if st.button("Download as CSV"):
            csv = df[df["status"].isin(filter_status)].to_csv(index=False)
            st.download_button("Click to Download", csv, "trading212_orders.csv", "text/csv")
    
    display_df = df[df["status"].isin(filter_status)][["dateCreated", "ticker", "quantity", "fillPrice", "cost", "status"]].copy()
    display_df.columns = ["Date", "Ticker", "Quantity", "Fill Price", "Cost", "Status"]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
