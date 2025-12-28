import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz

# --- DATA FROM EXCEL ---
SHARES = 431_344_811.58
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062 
EIGHT_STOCK_VALUE = 32_000_000
ETH_STAKED = 342_560
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
        # Fetching prices individually for maximum stability
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
    
    # Core NAV Calculations
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    nav_per_share = total_nav / SHARES
    mnav = (bmnr_p * SHARES) / total_nav
    
    # MNAV Ex-Cash (The Excel "MNAV-No Cash" Metric)
    nav_no_cash = total_nav - CASH
    mnav_no_cash = (bmnr_p * SHARES) / nav_no_cash if nav_no_cash > 0 else 0
    
    # Yield and Ratios
    total_annual_usd_yield = (ETH_STAKED * ANNUAL_STAKING_APR) * eth_p
    yield_per_share = total_annual_usd_yield / SHARES
    eth_per_share = ETH_HELD / SHARES

    # --- HEADER SECTION ---
    st.title("BMNR mNAV Tracker")
    
    est_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %I:%M:%S %p')
    st.markdown(f'<p class="timestamp">Last Updated: {est_time} EST</p>', unsafe_allow_html=True)

    # TOP METRICS (Added ETH/Share here)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1: st.metric("NAV/Share", f"${nav_per_share:,.2f}")
    with m2: st.metric("mNAV (Total)", f"{mnav:.3f}x")
    with m3: st.metric("mNAV (Ex-Cash)", f"{mnav_no_cash:.3f}x")
    with m4: st.metric("ETH/Share", f"{eth_per_share:.6f}")
    with m5: st.metric("Yield/Share", f"${yield_per_share:,.4f}")
    with m6: st.metric("BMNR Price", f"${bmnr_p:,.2f}")

    st.divider()

    # --- TREASURY BREAKDOWN ---
    st.subheader("Treasury & Staking Breakdown")
    
    assets_data = {
        "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
        "Total Quantity": [ETH_HELD, BTC_HELD, 0, 0],
        "Live Price": [eth_p, btc_p, 0, 0],
        "Staked Amount": [ETH_STAKED, 0, 0, 0],
        "Est. Annual Yield": [total_annual_usd_yield, 0, 0, 0],
        "Total Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
    }

    df = pd.DataFrame(assets_data)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            # format="%,.0f" adds commas and removes decimals as requested
            "Total Quantity": st.column_config.NumberColumn("Total Quantity", format="%,.0f"),
            "Live Price": st.column_config.NumberColumn("Live Price", format="$%,.0f"),
            "Staked Amount": st.column_config.NumberColumn("Staked Amount (ETH)", format="%,.0f"),
            "Est. Annual Yield": st.column_config.NumberColumn("Est. Annual Yield", format="$%,.0f"),
            "Total Value": st.column_config.NumberColumn("Total Value", format="$%,.0f"),
        }
    )
    
    # Secondary Info
    st.markdown("---")
    foot1, foot2 = st.columns(2)
    with foot1:
        st.write(f"**Total Shares:** {SHARES:,.0f}")
    with foot2:
        st.write(f"**Staking Utilization:** {(ETH_STAKED/ETH_HELD)*100:.2f}% of ETH portfolio")

    # Refresh
    time.sleep(60)
    st.rerun()

else:
    st.warning("🔄 Fetching live market data... Please wait.")
    time.sleep(5)
    st.rerun()
