import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- DATA UPDATED PER USER REQUEST ---
SHARES = 431_344_811.58
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062 
EIGHT_STOCK_VALUE = 32_000_000
ETH_STAKED = 342_560  # Updated value
ANNUAL_STAKING_APR = 0.03

st.set_page_config(page_title="BMNR NAV Tracker", page_icon="📈", layout="wide")

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p { color: #ADD8E6 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] div { color: #ADD8E6 !important; font-size: 2.2rem !important; }
    .timestamp { color: #888888; font-size: 0.9rem; margin-top: -20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30)
def fetch_prices():
    try:
        bmnr = yf.Ticker("BMNR").fast_info.last_price
        eth = yf.Ticker("ETH-USD").fast_info.last_price
        btc = yf.Ticker("BTC-USD").fast_info.last_price
        return bmnr, eth, btc
    except:
        return 0.0, 0.0, 0.0

bmnr_p, eth_p, btc_p = fetch_prices()

# --- CALCULATIONS ---
if bmnr_p > 0 and eth_p > 0:
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav
    
    total_annual_usd_yield = (ETH_STAKED * ANNUAL_STAKING_APR) * eth_p
    yield_per_share = total_annual_usd_yield / SHARES
    eth_per_share = ETH_HELD / SHARES

    # --- HEADER SECTION ---
    st.title("BMNR mNAV Tracker")
    est_time = datetime.now(pytz.timezone('
