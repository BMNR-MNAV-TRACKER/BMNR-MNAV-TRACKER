import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- BMNR DATA ---
SHARES = 425_841_924
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062  
EIGHT_STOCK_VALUE = 32_000_000
ETH_STAKED = 342_560  
ANNUAL_STAKING_APR = 0.030 

st.set_page_config(page_title="BMNR Tracker", page_icon="📈", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p { color: #ADD8E6 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] div { color: #ADD8E6 !important; font-size: 2.2rem !important; }
    .timestamp { color: #888888; font-size: 0.9rem; margin-top: -20px; }
    </style>
    """, unsafe_allow_html=True)

# --- RELIABLE PRICE FETCHING ---
def get_single_price(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Using fast_info is usually best for live trackers
        return ticker.fast_info.last_price
    except:
        return 0.0

# Fetch prices individually to prevent MultiIndex crashes
bmnr_p = get_single_price("BMNR")
eth_p = get_single_price("ETH-USD")
btc_p = get_single_price("BTC-USD")

# --- CALCULATIONS ---
if bmnr_p > 0 and eth_p > 0:
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav
    
    # Staking Yield
    total_annual_eth_yield = ETH_STAKED * ANNUAL_STAKING_APR
    total_annual_usd_yield = total_annual_eth_yield * eth_p
    yield_per_share = total_annual_usd_yield / SHARES
    
    # --- UI ---
    st.title("BMNR mNAV Tracker")
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %I:%M:%S %p')
    st.markdown(f'<p class="timestamp">Last Updated: {est_time} EST</p>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("NAV/Share", f"${nav_per_share:.2f}")
    m2.metric("mNAV Multiple", f"{mnav:.3f}x")
    m3.metric("Annual Yield/Share", f"${yield_per_share:.4f}")
    m4.metric("BMNR Price", f"${bmnr_p:.2f}")

    st.divider()

    st.subheader("Treasury & Staking Breakdown")
    assets_data = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Total Held": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
        "Live Price": [f"${eth_p:,.2f}", f"${btc_p:,.0f}", "-", "-"],
        "Staked Amount": [f"{ETH_STAKED:,} ETH", "0", "-", "-"],
        "Est. Annual Yield": [total_annual_usd_yield, 0, 0, 0],
        "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }

    st.dataframe(
        pd.DataFrame(assets_data),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Total Value": st.column_config.NumberColumn("Total Value", format="$%d"),
            "Est. Annual Yield": st.column_config.NumberColumn("Est. Annual Yield", format="$%d"),
        }
    )
else:
    st.error("Waiting for Yahoo Finance data... Check your internet or ticker symbols.")
    if st.button("Retry Now"):
        st.rerun()

# Auto-refresh
time.sleep(60)
st.rerun()
