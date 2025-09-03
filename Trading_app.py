import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import alpaca_trade_api as tradeapi

# Set page configuration
st.set_page_config(
    page_title="TradeVision - AI Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Alpaca API
API_KEY = "CKGJ7HZWSKG4WOEDY8Z7"
API_SECRET = "iMzuFeSgDm45ccDnlk6IR0OfXvWamndda9UvOl3p"
BASE_URL = "https://broker-api.sandbox.alpaca.markets"

# Initialize Alpaca API client
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

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
        transition: transform 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("TradeVision")
    st.markdown("---")
    
    menu_options = [
        "Dashboard", "Crypto Trading", "Day Trading", 
        "Options", "AI Trading Bots", "AI Games", 
        "AI Art Gallery", "Settings"
    ]
    
    icons = [
        "house", "coins", "exchange-alt", 
        "chart-bar", "robot", "gamepad", 
        "palette", "cog"
    ]
    
    selected_menu = st.radio(
        "Navigation",
        options=menu_options,
        format_func=lambda x: f"{x}",
        index=0
    )

# Header
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    st.title("TradeVision")
with col3:
    if st.button("Sign In", key="signin"):
        st.session_state.auth = True
    if st.button("Register", key="register"):
        st.session_state.auth = True

# Stats cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="stat-card"><h3>$42,137.89</h3><p>Portfolio Value</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><h3>+$1,243.23</h3><p>24h Change</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><h3>37</h3><p>Active Trades</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><h3>12</h3><p>AI Artworks</p></div>', unsafe_allow_html=True)

# Main content
st.markdown("---")

# Crypto Trading Section
st.header("Cryptocurrency Trading")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Market Data")
    
    # Sample crypto data (in a real app, you'd fetch this from an API)
    crypto_data = [
        {"name": "Bitcoin", "symbol": "BTC", "price": 37842.12, "change": 2.34},
        {"name": "Ethereum", "symbol": "ETH", "price": 2045.67, "change": 1.78},
        {"name": "Cardano", "symbol": "ADA", "price": 0.38, "change": -0.87},
        {"name": "Solana", "symbol": "SOL", "price": 41.23, "change": 5.12}
    ]
    
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
                    <div class="{change_class}">{change_icon} {abs(crypto['change'])}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Execute Trade")
    
    with st.form("trade_form"):
        asset = st.selectbox("Asset", ["BTC/USD", "ETH/USD", "ADA/USD", "SOL/USD"])
        amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
        leverage = st.selectbox("Leverage", ["1x", "2x", "5x", "10x"])
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
st.button("Generate New Art")

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

# Options Trading Section
st.header("Options Trading")
tab1, tab2, tab3 = st.tabs(["Call Options", "Put Options", "Strategies"])

with tab1:
    st.write("Trade call options based on market predictions.")
    
    option = st.selectbox("Select Option", [
        "AAPL 170C 12/15", 
        "TSLA 250C 12/22", 
        "NVDA 500C 01/05", 
        "SPY 450C 12/29"
    ])
    
    contracts = st.number_input("Number of Contracts", min_value=1, value=1)
    
    if st.button("Buy Call Option"):
        st.success(f"Bought {contracts} contract(s) of {option}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>TradeVision - AI Powered Trading Platform © 2023</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>This is a demonstration interface. Actual trading involves financial risk.</p>", unsafe_allow_html=True)

# Simulate live data updates
if 'price_data' not in st.session_state:
    st.session_state.price_data = crypto_data

# Function to update prices (simulated)
def update_prices():
    for crypto in st.session_state.price_data:
        change = (np.random.random() - 0.5) * 2
        crypto['change'] += change
        crypto['price'] *= (1 + change/100)
    
# Auto-refresh every 5 seconds
if st.button("Refresh Data"):
    update_prices()
    st.rerun()

# Auto-refresh every 30 seconds
if st.checkbox("Auto-refresh every 30 seconds"):
    time.sleep(30)
    update_prices()
    st.rerun()

# Alpaca API integration example
try:
    # Get account information
    account = api.get_account()
    st.sidebar.info(f"Account Status: {account.status}")
    
    # Get positions
    positions = api.list_positions()
    if positions:
        st.sidebar.subheader("Current Positions")
        for position in positions:
            st.sidebar.write(f"{position.symbol}: {position.qty} shares")
except Exception as e:
    st.sidebar.error(f"Error connecting to Alpaca: {e}")
