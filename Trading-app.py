import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import json

# Set page configuration
st.set_page_config(
    page_title="TradeVision - AI Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Alpha Vantage API keys to test
ALPHA_VANTAGE_KEYS = [
    "BE6N0Y60JC6H9J6M",
    "7FTFXJCGSMBORU0W"
]

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
    .key-status {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .key-valid {
        background-color: #10b98120;
        border-left: 4px solid #10b981;
    }
    .key-invalid {
        background-color: #ef444420;
        border-left: 4px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# Alpha Vantage API functions
def test_alpha_vantage_key(api_key):
    """Test if an Alpha Vantage API key works"""
    test_url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": "AAPL",
        "apikey": api_key
    }
    
    try:
        response = requests.get(test_url, params=params)
        data = response.json()
        
        if "Global Quote" in data:
            return True, "API key is working! ✅"
        elif "Note" in data and "API call frequency" in data["Note"]:
            return True, "API key is valid but rate limited ⚠️"
        elif "Error Message" in data:
            return False, f"Invalid API key ❌: {data['Error Message']}"
        else:
            return False, "Unknown API response ❌"
            
    except Exception as e:
        return False, f"Connection error: {str(e)} ❌"

def get_stock_price(symbol, api_key):
    """Get real-time stock price from Alpha Vantage"""
    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": api_key
        }
        
        response = requests.get("https://www.alphavantage.co/query", params=params)
        data = response.json()
        
        if "Global Quote" in data:
            return float(data["Global Quote"]["05. price"])
        else:
            return None
            
    except Exception as e:
        st.sidebar.error(f"Error fetching {symbol} price: {str(e)}")
        return None

def get_crypto_price(symbol, api_key):
    """Get cryptocurrency price from Alpha Vantage"""
    try:
        # Convert symbol to Alpha Vantage format (e.g., BTC->BTCUSD)
        crypto_symbol = f"{symbol}USD"
        
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": symbol,
            "to_currency": "USD",
            "apikey": api_key
        }
        
        response = requests.get("https://www.alphavantage.co/query", params=params)
        data = response.json()
        
        if "Realtime Currency Exchange Rate" in data:
            return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        else:
            return None
            
    except Exception as e:
        st.sidebar.error(f"Error fetching {symbol} price: {str(e)}")
        return None

def get_crypto_data(api_key):
    """Get cryptocurrency data with real prices"""
    crypto_symbols = ["BTC", "ETH", "ADA", "SOL"]
    crypto_data = []
    
    for symbol in crypto_symbols:
        current_price = get_crypto_price(symbol, api_key)
        
        if current_price is None:
            # Fallback to demo data if API fails
            demo_prices = {
                "BTC": 37842.12 + (np.random.random() - 0.5) * 1000,
                "ETH": 2045.67 + (np.random.random() - 0.5) * 50,
                "ADA": 0.38 + (np.random.random() - 0.5) * 0.05,
                "SOL": 41.23 + (np.random.random() - 0.5) * 2
            }
            current_price = demo_prices.get(symbol, 100.00)
        
        # Calculate random change for demo purposes
        price_change = (np.random.random() - 0.5) * 3
        
        crypto_data.append({
            "name": symbol,
            "symbol": symbol,
            "price": current_price,
            "change": price_change
        })
    
    return crypto_data

def get_stock_data(api_key):
    """Get stock data with real prices"""
    stock_symbols = ["AAPL", "TSLA", "NVDA", "SPY"]
    stock_data = []
    
    for symbol in stock_symbols:
        current_price = get_stock_price(symbol, api_key)
        
        if current_price is None:
            # Fallback to demo data if API fails
            demo_prices = {
                "AAPL": 170.00 + (np.random.random() - 0.5) * 2,
                "TSLA": 250.00 + (np.random.random() - 0.5) * 5,
                "NVDA": 500.00 + (np.random.random() - 0.5) * 10,
                "SPY": 450.00 + (np.random.random() - 0.5) * 3
            }
            current_price = demo_prices.get(symbol, 100.00)
        
        # Calculate random change for demo purposes
        price_change = (np.random.random() - 0.5) * 2
        
        stock_data.append({
            "name": symbol,
            "symbol": symbol,
            "price": current_price,
            "change": price_change
        })
    
    return stock_data

# Sidebar navigation and API key testing
with st.sidebar:
    st.title("TradeVision")
    st.markdown("---")
    
    # API Key Testing Section
    st.subheader("API Key Status")
    
    valid_keys = []
    for i, key in enumerate(ALPHA_VANTAGE_KEYS):
        # Display only first 5 and last 4 characters for security
        display_key = f"{key[:5]}...{key[-4:]}" if len(key) > 9 else key
        
        if st.button(f"Test Key {i+1}: {display_key}", key=f"test_key_{i}"):
            with st.spinner(f"Testing key {i+1}..."):
                is_valid, message = test_alpha_vantage_key(key)
                status_class = "key-valid" if is_valid else "key-invalid"
                st.markdown(f'<div class="key-status {status_class}">{message}</div>', unsafe_allow_html=True)
                
                if is_valid:
                    valid_keys.append(key)
                    st.session_state.valid_api_key = key
                    st.success(f"Using key {i+1} for data fetching!")
    
    # If we have valid keys, let user choose which one to use
    if valid_keys:
        st.markdown("---")
        selected_key = st.selectbox("Select API key to use:", valid_keys)
        st.session_state.selected_api_key = selected_key
    
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

# Header
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    st.title("TradeVision")
with col3:
    if st.button("Sign In", key="signin"):
        st.session_state.auth = True
    if st.button("Register", key="register"):
        st.session_state.auth = True

# Get live data using the selected API key
api_key = st.session_state.get('selected_api_key', None)

if api_key:
    crypto_data = get_crypto_data(api_key)
    stock_data = get_stock_data(api_key)
    st.sidebar.success(f"Using API key: {api_key[:5]}...{api_key[-4:]}")
else:
    # Use demo data if no API key is selected
    crypto_data = get_crypto_data(None)
    stock_data = get_stock_data(None)
    st.sidebar.warning("Using demo data - test and select an API key above")

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
    st.markdown(f'<div class="stat-card"><h3>{len(crypto_data) + len(stock_data)}</h3><p>Assets Tracked</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><h3>12</h3><p>AI Artworks</p></div>', unsafe_allow_html=True)

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
        
        st.markdown(f"""
        <div class="crypto-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #0f172a; 
                                display: flex; align-items: center; justify-content: center;">
                        {crypto['symbol'][0]}
                    </div>
                    <div>
                        <div><strong>{crypto['name']}</strong></div>
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
        
        st.markdown(f"""
        <div class="crypto-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #0f172a; 
                                display: flex; align-items: center; justify-content: center;">
                        {stock['symbol'][0]}
                    </div>
                    <div>
                        <div><strong>{stock['name']}</strong></div>
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
            asset = st.selectbox("Asset", ["BTC/USD", "ETH/USD", "ADA/USD", "SOL/USD"])
        else:
            asset = st.selectbox("Asset", ["AAPL", "TSLA", "NVDA", "SPY"])
            
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

# Auto-refresh
if st.button("Refresh Data"):
    st.rerun()

# Display API key status
if api_key:
    st.sidebar.success("Alpha Vantage API connected with real data!")
else:
    st.sidebar.warning("Using demo data - test API keys in sidebar")
