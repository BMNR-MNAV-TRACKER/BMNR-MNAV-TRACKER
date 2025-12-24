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

st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="wide")

# --- CUSTOM DESIGN (CSS) ---
# This makes the metric boxes look more professional
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 40px; color: #007BFF; }
    [data-testid="stMetricLabel"] { font-size: 18px; font-weight: bold; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30)
def fetch_prices():
    bmnr = yf.Ticker("BMNR").fast_info.last_price
    eth = yf.Ticker("ETH-USD").fast_info.last_price
    btc = yf.Ticker("BTC-USD").fast_info.last_price
    return bmnr, eth, btc

try:
    bmnr_p, eth_p, btc_p = fetch_prices()

    # Calculations
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav

    # --- THE TOP DESIGN (AS REQUESTED) ---
    st.title("Bitmine (BMNR) Dashboard")
    
    # Top Row: Primary Metrics
    t1, t2, t3 = st.columns(3)
    with t1:
        st.metric("NAV per Share", f"${nav_per_share:.2f}")
    with t2:
        # We can add a "delta" to show the multiple clearly
        st.metric("mNAV Multiple", f"{mnav:.3f}x", delta_color="off")
    with t3:
        st.metric("BMNR Market Price", f"${bmnr_p:.2f}")

    st.divider()

    # --- LOWER DESIGN: ASSET ALLOCATION ---
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Treasury Breakdown")
        df = pd.DataFrame({
            "Asset": ["Ethereum", "Bitcoin", "Cash", "Eightco"],
            "Amount": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
            "Price": [f"${eth_p:,.2f}", f"${btc_p:,.0f}", "-", "-"],
            "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
        })
        st.table(df.style.format({"Total Value": "${:,.0f}"}))

    with col2:
        st.subheader("Asset Allocation")
        # Quick visualization of where the money is
        chart_data = pd.DataFrame({
            "Source": ["ETH", "BTC", "Cash", "Other"],
            "Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
        }).set_index("Source")
        st.bar_chart(chart_data)

    # Footer
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
    st.caption(f"Market data synced via Yahoo Finance at {est_time} EST")

except Exception as e:
    st.error(f"Live Feed Interrupted: {e}")

# Auto-refresh logic
time.sleep(60)
st.rerun()
