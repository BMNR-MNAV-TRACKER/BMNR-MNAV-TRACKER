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
ETH_STAKED = 342_560  
ANNUAL_STAKING_APR = 0.030 

st.set_page_config(page_title="BMNR NAV Tracker", page_icon="📈", layout="wide")

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] p { color: #ADD8E6 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] div { color: #ADD8E6 !important; font-size: 2.2rem !important; }
    .timestamp { color: #888888; font-size: 0.9rem; margin-top: -20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
def fetch_price(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        return t.fast_info.last_price
    except:
        return 0.0

bmnr_p = fetch_price("BMNR")
eth_p = fetch_price("ETH-USD")
btc_p = fetch_price("BTC-USD")

# --- CALCULATIONS ---
if bmnr_p > 0 and eth_p > 0:
    val_eth = ETH_HELD * eth_p
    val_btc = BTC_HELD * btc_p
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav
    
    total_annual_usd_yield = (ETH_STAKED * ANNUAL_STAKING_APR) * eth_p
    yield_per_share = total_annual_usd_yield / SHARES

    # --- HEADER SECTION ---
    st.title("BMNR mNAV Tracker")
    
    # TIMESTAMP LINE
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %I:%M:%S %p')
    st.markdown(f'<p class="timestamp">Last Updated: {est_time} EST</p>', unsafe_allow_html=True)

    # METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("NAV/Share", f"${nav_per_share:.2f}")
    with m2: st.metric("mNAV Multiple", f"{mnav:.3f}x")
    with m3: st.metric("Annual Yield/Share", f"${yield_per_share:.4f}")
    with m4: st.metric("BMNR Price", f"${bmnr_p:.2f}")

    st.divider()

    # --- TREASURY BREAKDOWN TABLE ---
    st.subheader("Treasury & Staking Breakdown")
    
    assets_data = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Total Quantity": [ETH_HELD, BTC_HELD, 0, 0],
        "Live Price": [eth_p, btc_p, 0, 0],
        "Staked Amount": [ETH_STAKED, 0, 0, 0],
        "Est. Annual Yield": [total_annual_usd_yield, 0, 0, 0],
        "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Total Quantity": st.column_config.NumberColumn(
            "Total Quantity",
            format="%,.0f" # Commas and 0 decimals
        ),
        "Live Price": st.column_config.NumberColumn(
            "Live Price",
            format="$%,.0f" # Dollar sign, commas, and 0 decimals
        ),
        "Staked Amount (ETH)": st.column_config.NumberColumn(
            "Staked Amount (ETH)",
            format="%,.0f"
        ),
        "Est. Annual Yield": st.column_config.NumberColumn(
            "Est. Annual Yield",
            format="$%,.0f"
        ),
        "Total Value": st.column_config.NumberColumn(
            "Total Value",
            format="$%,.0f"
        ),
    }
)
    
time.sleep(60)
    st.rerun()

else:
    st.error("🔄 Connecting to Market Data... Please wait.")
    time.sleep(5)
    st.rerun()
