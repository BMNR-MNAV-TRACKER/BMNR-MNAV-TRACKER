import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import pytz
<button>Click Me</button>

# --- BMNR DATA ---
SHARES = 431_344_812
CASH = 1_000_000_000
BTC_HELD = 193
ETH_HELD = 4_066_062  
EIGHT_STOCK_VALUE = 32_000_000

st.set_page_config(page_title="BMNR mNAV Tracker", page_icon="📈", layout="wide")

# --- DATA FETCHING ---
@st.cache_data(ttl=30)
def fetch_prices():
    # Using a list to fetch all at once is slightly more efficient
    tickers = ["BMNR", "ETH-USD", "BTC-USD"]
    data = {}
    for t in tickers:
        data[t] = yf.Ticker(t).fast_info.last_price
    return data["BMNR"], data["ETH-USD"], data["BTC-USD"]

try:
    bmnr_price, eth_price, btc_price = fetch_prices()

    # Calculations
    val_eth = ETH_HELD * eth_price
    val_btc = BTC_HELD * btc_price
    total_nav = val_eth + val_btc + CASH + EIGHT_STOCK_VALUE
    
    # NEW METRICS
    nav_per_share = total_nav / SHARES
    market_cap = bmnr_price * SHARES
    mnav = market_cap / total_nav

    # --- TOP METRICS BAR ---
    st.title("Bitmine (BMNR) mNAV Tracker")
    
    # Create three clean columns for the header
    m1, m2, m3 = st.columns(3)
    
    # Column 1: NAV per Share
    m1.metric(label="NAV per Share", value=f"${nav_per_share:.2f}")
    
    # Column 2: mNAV Multiple
    # Helps visualize if BMNR is trading at a premium (>1) or discount (<1)
    m2.metric(label="mNAV Multiple", value=f"{mnav:.3f}x")
    
    # Column 3: Current BMNR Price
    m3.metric(label="BMNR Market Price", value=f"${bmnr_price:.2f}")

    st.divider()

    # --- BODY ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Treasury Breakdown")
        assets = {
            "Asset": ["Ethereum (ETH)", "Bitcoin (BTC)", "Cash", "Eightco Stake"],
            "Quantity": [f"{ETH_HELD:,}", f"{BTC_HELD:,}", "-", "-"],
            "Live Price": [f"${eth_price:,.2f}", f"${btc_price:,.0f}", "-", "-"],
            "Value": [val_eth, val_btc, CASH, EIGHT_STOCK_VALUE]
        }
        df = pd.DataFrame(assets)
        st.dataframe(
            df.style.format({"Value": "${:,.0f}"}), 
            use_container_width=True, 
            hide_index=True
        )

    with col_right:
        st.subheader("Market Info")
        st.write(f"**Total NAV:** ${total_nav / 1e9:.2f}B")
        st.write(f"**Market Cap:** ${market_cap / 1e9:.2f}B")
        
        # Time Logic
        est_tz = pytz.timezone('US/Eastern')
        est_time = datetime.now(est_tz).strftime('%I:%M:%S %p')
        st.caption(f"Last Updated: {est_time} EST")

except Exception as e:
    st.error(f"Error updating prices: {e}")

# --- AUTO-REFRESH ---
time.sleep(60)
st.rerun()
