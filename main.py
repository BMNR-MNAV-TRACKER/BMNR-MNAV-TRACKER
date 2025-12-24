import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- BMNR DATA ---
SHARES = 431_344_812
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062  
EIGHT_STOCK_VALUE = 32_000_000

st.set_page_config(page_title="BMNR Tracker", page_icon="📈", layout="wide")

# --- CUSTOM CSS FOR LIGHT BLUE METRICS & TIGHT SPACING ---
st.markdown("""
    <style>
    /* Light Blue for Metric Labels (Words) */
    [data-testid="stMetricLabel"] p {
        color: #ADD8E6 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    /* Light Blue for Metric Values (Numbers) */
    [data-testid="stMetricValue"] div {
        color: #ADD8E6 !important;
        font-size: 2.2rem !important;
    }
    /* Tighten column spacing */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        padding-right: 30px !important;
    }
    /* Style for the timestamp below title */
    .timestamp {
        color: #888888;
        font-size: 0.9rem;
        margin-top: -20px;
        margin-bottom: 20px;
    }
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

# Fetch Live Data
bmnr_p, eth_p, btc_p = fetch_prices()

# Calculations
val_eth = ETH_HELD * eth_p
val_btc = BTC_HELD * btc_p
total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
nav_per_share = total_nav / SHARES
mnav = (bmnr_p * SHARES) / total_nav

# --- HEADER SECTION ---
st.title("BMNR mNAV Tracker")

# Live Time Update below Title
est_tz = pytz.timezone('US/Eastern')
est_time = datetime.now(est_tz).strftime('%Y-%m-%d %I:%M:%S %p')
st.markdown(f'<p class="timestamp">Last Updated: {est_time} EST</p>', unsafe_allow_html=True)

# Top Metrics Row (Tight spacing)
m1, m2, m3, spacer = st.columns([1, 1, 1, 3])
with m1:
    st.metric("NAV/Share", f"${nav_per_share:.2f}")
with m2:
    st.metric("mNAV Multiple", f"{mnav:.3f}x")
with m3:
    st.metric("BMNR Price", f"${bmnr_p:.2f}")

st.divider()

# --- TREASURY BREAKDOWN TABLE ---
st.subheader("Treasury Breakdown")

# Creating the data with Quantity included
assets_data = {
    "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
    "Quantity": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
    "Live Price": [f"${eth_p:,.2f}", f"${btc_p:,.0f}", "-", "-"],
    "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
}

df = pd.DataFrame(assets_data)

# Formatting the Value column for display
st.table(df.style.format({"Total Value": "${:,.0f}"}))

# Auto-refresh
time.sleep(60)
st.rerun()
