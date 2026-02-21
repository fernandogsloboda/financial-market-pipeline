import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

# 2. Hero Section
st.title("📈 Financial Market Intelligence Dashboard")
st.markdown("Automated ETL Pipeline for Commodities and FX Analysis.")
st.markdown("---")

# 3. Sidebar Configuration
st.sidebar.header("⚙️ Analysis Parameters")
dias_historico = st.sidebar.slider("Select Timeframe (Days):", min_value=7, max_value=365, value=30)

# 4. Robust Data Extraction Function
@st.cache_data(ttl=3600)
def carregar_dados(dias):
    tickers = ["CL=F", "GC=F", "ZC=F", "BRL=X"]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=dias)
    
    # Robust download (works with latest yfinance version)
    df = yf.download(tickers, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        return pd.DataFrame()
        
    # Isolate Closing Prices
    close_prices = df['Close'].copy()
    
    # Ensure all columns exist
    for ticker in tickers:
        if ticker not in close_prices.columns:
            close_prices[ticker] = None
            
    close_prices = close_prices[tickers]
    close_prices.columns = ["Crude Oil (WTI)", "Gold", "Corn", "USD/BRL"]
    
    # Data Cleaning (Forward Fill for market holidays)
    return close_prices.ffill().dropna()

st.write(f"🔄 Extracting data for the last **{dias_historico} days** via Yahoo Finance API...")

# Execute Extraction
dados_limpos = carregar_dados(dias_historico)

# 5. Safety Shield & Display
if dados_limpos.empty:
    st.error("⚠️ Data returned empty. Yahoo Finance might be unstable or markets are closed. Try adjusting the timeframe in the sidebar.")
else:
    # Top Metrics Row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Price History (Raw Data)")
        st.dataframe(dados_limpos, use_container_width=True)

    with col2:
        st.subheader("📈 Daily Returns (%)")
        retornos = dados_limpos.pct_change().dropna() * 100
        st.dataframe(retornos.style.format("{:.2f}%"), use_container_width=True)

    # 6. Comparative Performance Chart (Base 100)
    st.markdown("---")
    st.subheader("📊 Comparative Performance (Base 100)")
    st.markdown("Visualization: If you had invested $100 in each asset at the start of the period, how much would it be worth today?")

    # Mathematical normalization
    dados_normalizados = (dados_limpos / dados_limpos.iloc[0]) * 100
    st.line_chart(dados_normalizados, height=400)

st.markdown("---")
st.caption("Disclaimer: This dashboard is for portfolio and educational purposes only. Data is provided by Yahoo Finance API.")
