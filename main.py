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

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p { color: #ADD8E6 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] div { color: #ADD8E6 !important; font-size: 2.2rem !important; }
    [data-testid="column"] { width: fit-content !important; flex: unset !important; padding-right: 30px !important; }
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

# Calculations
val_eth = ETH_HELD * eth_p
val_btc = BTC_HELD * btc_p
total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
nav_per_share = total_nav / SHARES
mnav = (bmnr_p * SHARES) / total_nav

# --- HEADER ---
st.title("BMNR mNAV Tracker")
est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %I:%M:%S %p')
st.markdown(f'<p class="timestamp">Last Updated: {est_time} EST</p>', unsafe_allow_html=True)

m1, m2, m3, spacer_top = st.columns([1, 1, 1, 3])
with m1: st.metric("NAV/Share", f"${nav_per_share:.2f}")
with m2: st.metric("mNAV Multiple", f"{mnav:.3f}x")
with m3: st.metric("BMNR Price", f"${bmnr_p:.2f}")

st.divider()

# --- NARROW TREASURY BREAKDOWN ---
st.subheader("Treasury Breakdown")

# We use 3 columns to center the table and keep it narrow
# [0.1, 0.8, 0.1] means the side columns are 10% each and the table is 80%
# You can change this to [1, 2, 1] for even narrower (50% table)
col_spacer_l, col_main, col_spacer_r = st.columns([0.05, 0.9, 2]) 

with col_main:
    assets_data = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Quantity": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
        "Live Price": [f"${eth_p:,.2f}", f"${btc_p:,.0f}", "-", "-"],
        "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }
    df = pd.DataFrame(assets_data)
    
    # st.dataframe with column_config is the most modern way to format
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Total Value": st.column_config.NumberColumn(format="$%d"),
            "Asset": st.column_config.Column(width="medium"),
            "Quantity": st.column_config.Column(width="small"),
        }
    )

time.sleep(60)
st.rerun()
