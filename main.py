import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- BMNR DATA (2025 Record Date Update) ---
SHARES = 425_841_924
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062  
EIGHT_STOCK_VALUE = 32_000_000
ETH_STAKED = 342_560  
ANNUAL_STAKING_APR = 0.034 

st.set_page_config(page_title="BMNR NAV Tracker", page_icon="📈", layout="wide")

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p { color: #ADD8E6 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] div { color: #ADD8E6 !important; font-size: 2.2rem !important; }
    .timestamp { color: #888888; font-size: 0.9rem; margin-top: -20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA FETCHING ---
def fetch_price(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        # 2025 preferred method for single-price stability
        return t.fast_info.last_price
    except:
        return 0.0

bmnr_p = fetch_price("BMNR")
eth_p = fetch_price("ETH-USD")
btc_p = fetch_price("BTC-USD")

# --- CORE CALCULATIONS ---
if bmnr_p > 0 and eth_p > 0:
    # Value Calculations
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav
    
    # Staking Yield Calculations
    total_annual_usd_yield = (ETH_STAKED * ANNUAL_STAKING_APR) * eth_p
    yield_per_share = total_annual_usd_yield / SHARES

    # --- HEADER SECTION ---
    st.title("BMNR mNAV Tracker")
    est_time = datetime.now(pytz.timezone('
