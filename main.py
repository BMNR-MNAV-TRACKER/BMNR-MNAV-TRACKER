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

# --- CUSTOM CSS FOR LIGHT BLUE METRICS ---
st.markdown("""
    <style>
    /* Target the Metric Labels (the words) */
    [data-testid="stMetricLabel"] p {
        color: #ADD8E6 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    /* Target the Metric Values (the numbers) */
    [data-testid="stMetricValue"] div {
        color: #ADD8E6 !important;
        font-size: 2.5rem !important;
    }
    /* Reduce spacing between metrics */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        padding-right: 40px !important;
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

# Fetch Data
bmnr_p, eth_p, btc_p = fetch_prices()

# Calculations
val_eth = ETH_HELD * eth_p
val_btc = BTC_HELD * btc_p
total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
nav_per_share = total_nav / SHARES
mnav = (bmnr_p * SHARES) / total_nav

# --- TOP METRICS ROW ---
# Using 5 columns but only filling 3 to keep them "close together" on the left
m1, m2, m3, spacer = st.columns([1, 1, 1, 3])

with m1:
    st.metric("NAV/Share", f"${nav_per_share:.2f}")
with m2:
    st.metric("mNAV", f"{mnav:.3f}x")
with m3:
    st.metric("BMNR Price", f"${bmnr_p:.2f}")

st.divider()

# --- TABLE BREAKDOWN ---
st.subheader("Treasury Breakdown")
df = pd.DataFrame({
    "Asset": ["Ethereum", "Bitcoin", "Cash", "Eightco"],
    "Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
})

# Display as a clean table
st.table(df.style.format({"Value": "${:,.0f}"}))

# Time sync
est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%I:%M:%S %p')
st.caption(f"Last Updated: {est_time} EST")
