import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="TradeVision - AI Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to style the app
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .sidebar .sidebar-content {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
    }
    .card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .crypto-item {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .price-up {
        color: #10b981;
    }
    .price-down {
        color: #ef4444;
    }
    .stat-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .art-item {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        overflow: hidden;
    }
    .data-status {
        padding: 8px 12px;
        border-radius: 6px;
        margin: 5px 0;
        font-size: 0.9rem;
    }
    .status-success {
        background-color: #10b98120;
        border-left: 4px solid #10b981;
    }
    .status-warning {
        background-color: #f59e0b20;
        border-left: 4px solid #f59e0b;
    }
    .refresh-timer {
        background-color: #0366d620;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 10px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Alternative data source functions (no yfinance needed)
def get_crypto_price(symbol):
    """Get cryptocurrency price from alternative source"""
    try:
        # Try to get data from CoinGecko API (no API key needed)
        if symbol == "BTC":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['bitcoin']['usd'], True
        elif symbol == "ETH":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['ethereum']['usd'], True
        elif symbol == "ADA":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['cardano']['usd'], True
        elif symbol == "SOL":
            url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            return data['solana']['usd'], True
    except:
        pass
    
    # Fallback to demo data
    demo_prices = {
        "BTC": 37842.12 + (np.random.random() - 0.5) * 1000,
        "ETH": 2045.67 + (np.random.random() - 0.5) * 50,
        "ADA": 0.38 + (np.random.random() - 0.5) * 0.05,
        "SOL": 41.23 + (np.random.random() - 0.5) * 2,
        "DOGE": 0.08 + (np.random.random() - 0.5) * 0.01
    }
    return demo_prices.get(symbol, 100.00), False

def get_stock_price(symbol):
    """Get stock price from alternative source"""
    try:
        # Try to get data from Financial Modeling Prep (free tier)
        if symbol in ["AAPL", "TSLA", "NVDA", "SPY", "MSFT", "GOOGL"]:
            url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=demo"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data and len(data) > 0:
                return data[0]['price'], True
    except:
        pass
    
    # Fallback to demo data
    demo_prices = {
        "AAPL": 170.00 + (np.random.random() - 0.5) * 2,
        "TSLA": 250.00 + (np.random.random() - 0.5) * 5,
        "NVDA": 500.00 + (np.random.random() - 0.5) * 10,
        "SPY": 450.00 + (np.random.random() - 0.5) * 3,
        "MSFT": 330.00 + (np.random.random() - 0.5) * 2,
        "GOOGL": 130.00 + (np.random.random() - 0.5) * 1
    }
    return demo_prices.get(symbol, 100.00), False

def get_stock_data():
    """Get stock data with real prices"""
    stock_symbols = ["AAPL", "TSLA", "NVDA", "SPY", "MSFT", "GOOGL"]
    stock_data = []
    live_data_count = 0
    
    for symbol in stock_symbols:
        current_price, is_live = get_stock_price(symbol)
        
        # Calculate random change for demo purposes
        price_change = (np.random.random() - 0.5) * 2
        
        if is_live:
            live_data_count += 1
        
        stock_data.append({
            "name": symbol,
            "symbol": symbol,
            "price": current_price,
            "change": price_change,
            "is_live": is_live
        })
    
    return stock_data, live_data_count

def get_crypto_data():
    """Get cryptocurrency data with real prices"""
    crypto_symbols = ["BTC", "ETH", "ADA", "SOL", "DOGE"]
    crypto_data = []
    live_data_count = 0
    
    for symbol in crypto_symbols:
        current_price, is_live = get_crypto_price(symbol)
        
        # Calculate random change for demo purposes
        price_change = (np.random.random() - 0.5) * 3
        
        if is_live:
            live_data_count += 1
        
        crypto_data.append({
            "name": symbol,
            "symbol": symbol,
            "price": current_price,
            "change": price_change,
            "is_live": is_live
        })
    
    return crypto_data, live_data_count

# Sidebar navigation
with st.sidebar:
    st.title("TradeVision")
    st.markdown("---")
    
    menu_options = [
        "Dashboard", "Crypto Trading", "Stock Trading", 
        "Options", "AI Trading Bots", "AI Games", 
        "AI Art Gallery", "Settings"
    ]
    
    selected_menu = st.radio(
        "Navigation",
        options=menu_options,
        index=0
    )
    
    # Display account info (demo data)
    st.markdown("---")
    st.subheader("Account Overview")
    st.write("Status: **ACTIVE**")
    st.write("Buying Power: **$100,000.00**")
    st.write("Cash: **$25,000.00**")
    st.write("Portfolio Value: **$42,137.89**")
    
    # Data status
    st.markdown("---")
    st.subheader("Data Status")
    st.markdown('<div class="data-status status-success">Using Public APIs</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-status status-success">No API key required</div>', unsafe_allow_html=True)
    st.markdown('<div class="data-status status-warning">Some data may be delayed</div>', unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    st.title("TradeVision")
with col3:
    if st.button("Sign In", key="signin"):
        st.session_state.auth = True
    if st.button("Register", key="register"):
        st.session_state.auth = True

# Get live data
crypto_data, crypto_live_count = get_crypto_data()
stock_data, stock_live_count = get_stock_data()
total_live_data = crypto_live_count + stock_live_count
total_assets = len(crypto_data) + len(stock_data)

# Stats cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

# Calculate portfolio stats
portfolio_value = 42137.89
daily_change = (np.random.random() - 0.5) * 3  # Random change for demo

with col1:
    st.markdown(f'<div class="stat-card"><h3>${portfolio_value:,.2f}</h3><p>Portfolio Value</p></div>', unsafe_allow_html=True)
with col2:
    change_color = "price-up" if daily_change >= 0 else "price-down"
    change_icon = "▲" if daily_change >= 0 else "▼"
    st.markdown(f'<div class="stat-card"><h3><span class="{change_color}">{change_icon} {abs(daily_change):.2f}%</span></h3><p>24h Change</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><h3>{total_assets}</h3><p>Assets Tracked</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-card"><h3>{total_live_data}/{total_assets}</h3><p>Live Data Sources</p></div>', unsafe_allow_html=True)

# Data status indicator
if total_live_data == total_assets:
    st.success("✅ All data is live from external APIs")
elif total_live_data > 0:
    st.warning(f"⚠️ {total_live_data}/{total_assets} assets using live data (some using demo data)")
else:
    st.error("❌ Using demo data - check internet connection")

# Main content
st.markdown("---")

# Crypto Trading Section
st.header("Cryptocurrency Trading")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Live Crypto Data")
    
    for crypto in crypto_data:
        change_class = "price-up" if crypto["change"] >= 0 else "price-down"
        change_icon = "▲" if crypto["change"] >= 0 else "▼"
        live_indicator = "✅" if crypto["is_live"] else "📊"
        
        st.markdown(f"""
        <div class="crypto-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #0f172a; 
                                display: flex; align-items: center; justify-content: center;">
                        {crypto['symbol'][0]}
                    </div>
                    <div>
                        <div><strong>{crypto['name']}</strong> {live_indicator}</div>
                        <div>{crypto['symbol']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div>${crypto['price']:,.2f}</div>
                    <div class="{change_class}">{change_icon} {abs(crypto['change']):.2f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Stock Trading Section
st.header("Stock Trading")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Live Stock Data")
    
    for stock in stock_data:
        change_class = "price-up" if stock["change"] >= 0 else "price-down"
        change_icon = "▲" if stock["change"] >= 0 else "▼"
        live_indicator = "✅" if stock["is_live"] else "📊"
        
        st.markdown(f"""
        <div class="crypto-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #0f172a; 
                                display: flex; align-items: center; justify-content: center;">
                        {stock['symbol'][0]}
                    </div>
                    <div>
                        <div><strong>{stock['name']}</strong> {live_indicator}</div>
                        <div>{stock['symbol']}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div>${stock['price']:,.2f}</div>
                    <div class="{change_class}">{change_icon} {abs(stock['change']):.2f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Execute Trade")
    
    with st.form("trade_form"):
        asset_type = st.selectbox("Asset Type", ["Crypto", "Stocks"])
        
        if asset_type == "Crypto":
            asset = st.selectbox("Asset", ["BTC/USD", "ETH/USD", "ADA/USD", "SOL/USD", "DOGE/USD"])
        else:
            asset = st.selectbox("Asset", ["AAPL", "TSLA", "NVDA", "SPY", "MSFT", "GOOGL"])
            
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
        order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop Loss"])
        
        col1, col2 = st.columns(2)
        with col1:
            buy_button = st.form_submit_button("Buy")
        with col2:
            sell_button = st.form_submit_button("Sell")
    
    if buy_button:
        st.success(f"Buy order placed for {amount} of {asset}")
    if sell_button:
        st.error(f"Sell order placed for {amount} of {asset}")

# AI Art Gallery Section
st.header("AI Art Gallery")
if st.button("Generate New Art"):
    st.success("Generating new AI artwork...")

art_cols = st.columns(4)
artworks = [
    {"title": "Cosmic Dream", "date": "Generated 2 days ago"},
    {"title": "Neural Landscape", "date": "Generated 5 days ago"},
    {"title": "Digital Abyss", "date": "Generated 1 week ago"},
    {"title": "Quantum Forest", "date": "Generated 3 days ago"}
]

for i, art in enumerate(artworks):
    with art_cols[i]:
        st.markdown(f"""
        <div class="art-item">
            <div style="height: 150px; background: linear-gradient(45deg, #6366f1, #8b5cf6); 
                        display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 3rem;">🖼️</span>
            </div>
            <div style="padding: 15px;">
                <div style="font-weight: 600; margin-bottom: 5px;">{art['title']}</div>
                <div style="font-size: 0.9rem; color: #94a3b8;">{art['date']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>TradeVision - AI Powered Trading Platform © 2023</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>This is a demonstration interface. Actual trading involves financial risk.</p>", unsafe_allow_html=True)

# Auto-refresh button
if st.button("🔄 Refresh Data Now"):
    st.rerun()

# Automatic refresh every 60 seconds
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Check if 60 seconds have passed since last refresh
if time.time() - st.session_state.last_refresh > 60:
    st.session_state.last_refresh = time.time()
    st.rerun()

# Display countdown timer
seconds_until_refresh = 60 - (time.time() - st.session_state.last_refresh)
st.sidebar.markdown(f'<div class="refresh-timer">⏱️ Auto-refresh in: {int(seconds_until_refresh)} seconds</div>', unsafe_allow_html=True)

# Data source info
st.sidebar.markdown("---")
st.sidebar.info("""
**Data Sources:** CoinGecko API + Financial Modeling Prep  
**No API Key Required**  
**Rate Limits:** Minimal (free tiers)  
**Data Delay:** Real-time or slight delay
**Auto-Refresh:** Every 60 seconds
""")
