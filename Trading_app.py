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

# Securely access Alpaca API details from Streamlit secrets
try:
    API_KEY = st.secrets["alpaca"]["api_key"]
    API_SECRET = st.secrets["alpaca"]["api_secret"]
    BASE_URL = "https://broker-api.sandbox.alpaca.markets"
    DATA_URL = "https://data.sandbox.alpaca.markets"
    
    # Verify we got the keys (but don't display them)
    if API_KEY and API_SECRET:
        st.sidebar.success("Alpaca API keys loaded securely")
    else:
        st.sidebar.error("API keys not found in secrets")
        
except Exception as e:
    st.sidebar.error(f"Error loading API keys: {str(e)}")
    # Fallback to empty keys (app will still work with demo data)
    API_KEY = ""
    API_SECRET = ""
    BASE_URL = "https://broker-api.sandbox.alpaca.markets"
    DATA_URL = "https://data.sandbox.alpaca.markets"

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
</style>
""", unsafe_allow_html=True)

# Alpaca API functions
def get_account_info():
    """Get Alpaca account information"""
    try:
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        response = requests.get(f"{BASE_URL}/v2/account", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.sidebar.error(f"Account API Error: {response.status_code}")
            return None
    except Exception as e:
        st.sidebar.error(f"Error fetching account info: {str(e)}")
        return None

def get_crypto_data(symbols=['BTC/USD', 'ETH/USD', 'ADA/USD', 'SOL/USD']):
    """Get cryptocurrency data from Alpaca"""
    crypto_data = []
    
    for symbol in symbols:
        try:
            # For sandbox, we'll use mock data since crypto might not be available
            # In a real implementation, you'd use: f"{DATA_URL}/v1beta3/crypto/{symbol}/trades"
            base_symbol = symbol.split('/')[0]
            
            # Mock data for demonstration
            mock_prices = {
                'BTC': 37842.12 + (np.random.random() - 0.5) * 1000,
                'ETH': 2045.67 + (np.random.random() - 0.5) * 50,
                'ADA': 0.38 + (np.random.random() - 0.5) * 0.05,
                'SOL': 41.23 + (np.random.random() - 0.5) * 2
            }
            
            mock_changes = {
                'BTC': 2.34 + (np.random.random() - 0.5) * 1,
                'ETH': 1.78 + (np.random.random() - 0.5) * 0.8,
                'ADA': -0.87 + (np.random.random() - 0.5) * 0.5,
                'SOL': 5.12 + (np.random.random() - 0.5) * 1.2
            }
            
            crypto_data.append({
                "name": f"{base_symbol}",
                "symbol": base_symbol,
                "price": mock_prices.get(base_symbol, 100),
                "change": mock_changes.get(base_symbol, 0)
            })
            
        except Exception as e:
            st.sidebar.error(f"Error fetching {symbol}: {str(e)}")
    
    return crypto_data

def get_positions():
    """Get current positions from Alpaca"""
    try:
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        response = requests.get(f"{BASE_URL}/v2/positions", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return []  # Return empty list if no positions or error
    except Exception as e:
        st.sidebar.error(f"Error fetching positions: {str(e)}")
        return []

# Sidebar navigation
with st.sidebar:
    st.title("TradeVision")
    st.markdown("---")
    
    menu_options = [
        "Dashboard", "Crypto Trading", "Day Trading", 
        "Options", "AI Trading Bots", "AI Games", 
        "AI Art Gallery", "Settings"
    ]
    
    selected_menu = st.radio(
        "Navigation",
        options=menu_options,
        index=0
    )
    
    # Display account info if available
    account_info = get_account_info()
    if account_info:
        st.markdown("---")
        st.subheader("Account Overview")
        st.write(f"Status: **{account_info.get('status', 'N/A')}**")
        st.write(f"Buying Power: **${float(account_info.get('buying_power', 0)):,.2f}**")
        st.write(f"Cash: **${float(account_info.get('cash', 0)):,.2f}**")
        st.write(f"Portfolio Value: **${float(account_info.get('portfolio_value', 0)):,.2f}**")

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
crypto_data = get_crypto_data()
positions = get_positions()

# Stats cards
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

# Calculate portfolio stats
portfolio_value = float(account_info['portfolio_value']) if account_info else 42137.89
cash_value = float(account_info['cash']) if account_info else 10000.00
daily_change = (portfolio_value - 42137.89) / 42137.89 * 100 if account_info else 2.95

with col1:
    st.markdown(f'<div class="stat-card"><h3>${portfolio_value:,.2f}</h3><p>Portfolio Value</p></div>', unsafe_allow_html=True)
with col2:
    change_color = "price-up" if daily_change >= 0 else "price-down"
    change_icon = "▲" if daily_change >= 0 else "▼"
    st.markdown(f'<div class="stat-card"><h3><span class="{change_color}">{change_icon} {abs(daily_change):.2f}%</span></h3><p>24h Change</p></div>', unsafe_allow_html=True)
with col3:
    positions_count = len(positions) if positions else 3
    st.markdown(f'<div class="stat-card"><h3>{positions_count}</h3><p>Active Trades</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-card"><h3>12</h3><p>AI Artworks</p></div>', unsafe_allow_html=True)

# Main content
st.markdown("---")

# Crypto Trading Section
st.header("Cryptocurrency Trading")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Live Market Data")
    
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
        # In a real app: api.submit_order(symbol=asset, qty=amount, side='buy', type='market')
    if sell_button:
        st.error(f"Sell order placed for {amount} of {asset}")
        # In a real app: api.submit_order(symbol=asset, qty=amount, side='sell', type='market')

# Display current positions if available
if positions:
    st.subheader("Your Positions")
    for position in positions:
        st.write(f"{position['symbol']}: {position['qty']} shares - P/L: ${position['unrealized_pl']}")

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

# Auto-refresh
if st.button("Refresh Data"):
    st.rerun()

# Note about sandbox mode
st.sidebar.info("Using Alpaca Sandbox Mode - Trades are simulated")
