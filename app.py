import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Alpha Market Intelligence Pro", layout="wide")

# --- 2. PREMIUM CSS (FIXED CONTRAST & LAYOUT) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Metric Cards Styling */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border: 1px solid #e6e9ef !important;
    }
    /* Force Text Color for Metrics (Black/Dark Gray) */
    [data-testid="stMetricLabel"] p {
        color: #555e6d !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] div {
        color: #1f2937 !important;
        font-weight: bold !important;
    }
    /* Section Dividers */
    hr { margin-top: 2rem; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
st.sidebar.title("📊 Control Panel")
st.sidebar.markdown("Configure analysis timeframe and indicators.")
dias_historico = st.sidebar.slider("Analysis Period (Days)", 7, 365, 60)
show_sma = st.sidebar.checkbox("Show 20-Day Moving Average", value=False)

@st.cache_data(ttl=3600)
def fetch_data(dias):
    tickers = ["CL=F", "GC=F", "ZC=F", "BRL=X"]
    start = datetime.today() - timedelta(days=dias)
    df = yf.download(tickers, start=start, end=datetime.today(), progress=False)
    if df.empty: return pd.DataFrame()
    prices = df['Close'].copy()
    prices.columns = ["Crude Oil", "Gold", "Corn", "USD/BRL"]
    return prices.ffill().dropna()

# --- 4. CORE LOGIC ---
data = fetch_data(dias_historico)

if not data.empty:
    st.title("🏛️ Alpha Market Intelligence Pro")
    st.caption(f"Real-time ETL Pipeline | Last Sync: {datetime.now().strftime('%H:%M:%S')}")
    
    # --- SECTION 1: KEY METRICS ---
    st.subheader("📌 Current Market Snapshot")
    cols = st.columns(4)
    for i, asset in enumerate(data.columns):
        curr, prev = data[asset].iloc[-1], data[asset].iloc[-2]
        delta = ((curr - prev) / prev) * 100
        cols[i].metric(label=asset, value=f"{curr:.2f}", delta=f"{delta:.2f}%")

    st.markdown("---")

    # --- SECTION 2: PERFORMANCE ANALYSIS ---
    col_chart, col_stat = st.columns([3, 1])
    with col_chart:
        st.subheader("📈 Normalized Performance (Base 100)")
        norm = (data / data.iloc[0]) * 100
        
        if show_sma:
            for col in data.columns:
                norm[f"{col} (SMA 20)"] = norm[col].rolling(window=20).mean()
        
        st.line_chart(norm, height=450)
        
    with col_stat:
        st.subheader("Period Summary")
        total_ret = ((data.iloc[-1] / data.iloc[0]) - 1) * 100
        for asset, ret in total_ret.items():
            color = "green" if ret > 0 else "red"
            st.markdown(f"**{asset}**: :{color}[{ret:.2f}%]")
        
        st.divider()
        st.info(f"🏆 **Best:** {total_ret.idxmax()}")
        st.warning(f"📉 **Worst:** {total_ret.idxmin()}")

    st.markdown("---")

    # --- SECTION 3: RISK & CORRELATION (UNIFIED) ---
    st.subheader("🎯 Risk & Correlation Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Correlation Matrix**")
        corr = data.pct_change().corr()
        st.dataframe(corr.style.background_gradient(cmap='RdYlGn').format("{:.2f}"), use_container_width=True)
    with c2:
        st.markdown("**Annualized Volatility (%)**")
        vol = data.pct_change().std() * np.sqrt(252) * 100
        st.bar_chart(vol)

    # --- SECTION 4: DATA EXPORT ---
    st.markdown("---")
    with st.expander("📥 View Raw Data and Export"):
        st.dataframe(data, use_container_width=True)
        csv = data.to_csv().encode('utf-8')
        st.download_button("Export to CSV", csv, "market_data.csv", "text/csv")

else:
    st.error("Failed to retrieve market data. Please check your connection.")

st.markdown("---")
st.caption("Developed for Professional Portfolio | Data: Yahoo Finance API")
