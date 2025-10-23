import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import base64
import re

st.set_page_config(page_title="Trading212 Advanced Analytics", layout="wide")

st.title("Trading212 Advanced Portfolio Analytics")
st.markdown("*Real-time interactive dashboard for your Trading212 portfolio*")

if "orders_data" not in st.session_state:
    st.session_state.orders_data = None

def fetch_trading212_data(api_key, api_secret, domain="https://live.trading212.com"):
    """Fetch all order history from Trading212 API"""
    all_items = []
    cursor = 0
    
    credentials = f"{api_key}:{api_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json"
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    while True:
        try:
            url = f"{domain}/api/v0/equity/history/orders?cursor={cursor}&limit=50"
            status_text.text(f"Fetching orders... Total so far: {len(all_items)}")
            
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code != 200:
                st.error(f"API Error: {resp.status_code}")
                break
            
            data = resp.json()
            items = data.get("items", [])
            
            if not items:
                break
            
            all_items.extend(items)
            
            next_path = data.get("nextPagePath")
            if not next_path:
                break
            
            match = re.search(r'cursor=(\d+)', next_path)
            if match:
                cursor = int(match.group(1))
            else:
                break
            
            progress_bar.progress(min(len(all_items) / 500, 0.95))
        
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            break
    
    progress_bar.progress(1.0)
    status_text.text(f"Loaded {len(all_items)} orders!")
    
    return all_items

# Try to get credentials from Streamlit secrets
try:
    api_key = st.secrets["T212_API_KEY"]
    api_secret = st.secrets["T212_API_SECRET"]
    has_secrets = True
except (KeyError, FileNotFoundError):
    api_key = None
    api_secret = None
    has_secrets = False

# Sidebar
with st.sidebar:
    st.header("API Configuration")
    
    if has_secrets:
        st.success("✓ Secrets loaded")
        if st.button("Reload Data from Trading212"):
            with st.spinner("Fetching your portfolio data..."):
                orders_data = fetch_trading212_data(api_key, api_secret)
                
                if orders_data:
                    st.session_state.orders_data = orders_data
                    st.success(f"Loaded {len(orders_data)} orders!")
                    st.rerun()
    else:
        st.warning("No secrets found. Enter credentials manually:")
        api_key = st.text_input("API Key", type="password")
        api_secret = st.text_input("API Secret", type="password")
        
        if st.button("Load Data from Trading212"):
            if api_key and api_secret:
                with st.spinner("Fetching your portfolio data..."):
                    orders_data = fetch_trading212_data(api_key, api_secret)
                    
                    if orders_data:
                        st.session_state.orders_data = orders_data
                        st.success(f"Loaded {len(orders_data)} orders!")
                        st.rerun()
            else:
                st.error("Please enter both API Key and Secret")

# Auto-load if secrets are available and data not loaded
if has_secrets and not st.session_state.orders_data:
    with st.spinner("Loading your portfolio data from Trading212..."):
        orders_data = fetch_trading212_data(api_key, api_secret)
        
        if orders_data:
            st.session_state.orders_data = orders_data

# Check if data is loaded
if st.session_state.orders_data:
    orders_data = st.session_state.orders_data
    
    # Process data
    df = pd.DataFrame(orders_data)
    df["dateCreated"] = pd.to_datetime(df["dateCreated"])
    df["ticker"] = df["ticker"].str.replace("_US_EQ", "").str.replace("_EQ", "")
    df["cost"] = df.get("fillCost", df.get("orderedValue", 0)).fillna(0)
    df["quantity"] = df.get("filledQuantity", 0).fillna(0)
    df["fillPrice"] = df.get("fillPrice", 0).fillna(0)
    df["avg_price_per_share"] = (df["cost"] / df["quantity"]).replace([np.inf, -np.inf], 0).fillna(0)
    
    df_filled = df[df["status"] == "FILLED"].copy()
    
    # Sidebar filters
    with st.sidebar:
        st.divider()
        st.header("Filters")
        date_range = st.date_input(
            "Date range",
            value=(df["dateCreated"].min().date(), df["dateCreated"].max().date()),
        )
        selected_tickers = st.multiselect(
            "Tickers",
            sorted(df_filled["ticker"].unique()),
            default=sorted(df_filled["ticker"].unique())
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
            stock_sorted = stock_data.sort_values("dateCreated")
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

else:
    st.info("Enter your Trading212 API credentials in the sidebar to load your portfolio data.")
