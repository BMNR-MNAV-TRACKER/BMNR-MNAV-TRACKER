import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- BMNR DATA (Updated Dec 2025) ---
SHARES = 425_841_924  # Per SEC Record Date Dec 8, 2025
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062  
EIGHT_STOCK_VALUE = 32_000_000

# Staking Data
ETH_STAKED = 342_560  # Initial pilot amount (MAVAN scale-up early 2026)
ANNUAL_STAKING_APR = 0.034  # 3.4% Est. Yield

st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="wide")

# --- CUSTOM CSS ---
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
        # Fetching as a group is more reliable
        data = yf.download(tickers="BMNR ETH-USD BTC-USD", period="1d", interval="1m", progress=False)
        bmnr = data['Close']['BMNR'].iloc[-1]
        eth = data['Close']['ETH-USD'].iloc[-1]
        btc = data['Close']['BTC-USD'].iloc[-1]
        return bmnr, eth, btc
    except:
        return 0.0, 0.0, 0.0

bmnr_p, eth_p, btc_p = fetch_prices()

# --- CALCULATIONS ---
if eth_p > 0:
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav if total_nav > 0 else 0
    
    # Staking Yield Calculations
    total_annual_eth_yield = ETH_STAKED * ANNUAL_STAKING_APR
    total_annual_usd_yield = total_annual_eth_yield * eth_p
    yield_per_share = total_annual_usd_yield / SHARES
else:
    # Error state placeholders
    total_nav, nav_per_share, mnav, yield_per_share = 0, 0, 0, 0
    val_eth, val_btc = 0, 0
    total_annual_usd_yield
