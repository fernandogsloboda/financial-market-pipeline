import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Intelligence Pro", layout="wide")

# --- CUSTOM CSS FOR BETTER VISUALS ---
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_base_curve=True)

st.title("📈 Professional Market Intelligence Dashboard")
st.markdown("Automated ETL & Quantitative Analytics for Global Assets.")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Analysis Parameters")
dias_historico = st.sidebar.slider("Select Timeframe (Days):", min_value=7, max_value=365, value=30)

@st.cache_data(ttl=3600)
def carregar_dados(dias):
    tickers = ["CL=F", "GC=F", "ZC=F", "BRL=X"]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=dias)
    df = yf.download(tickers, start=start_date, end=end_date, progress=False)
    
    if df.empty: return pd.DataFrame()
        
    close_prices = df['Close'].copy()
    for ticker in tickers:
        if ticker not in close_prices.columns: close_prices[ticker] = None
            
    close_prices = close_prices[tickers]
    close_prices.columns = ["Crude Oil (WTI)", "Gold", "Corn", "USD/BRL"]
    return close_prices.ffill().dropna()

dados_limpos = carregar_dados(dias_historico)

if dados_limpos.empty:
    st.error("⚠️ Data connection failed. Please try again.")
else:
    # --- SECTION 1: KEY PERFORMANCE INDICATORS (KPIs) ---
    st.subheader("📌 Current Market Snapshot")
    cols = st.columns(4)
    
    for i, asset in enumerate(dados_limpos.columns):
        current_price = dados_limpos[asset].iloc[-1]
        previous_price = dados_limpos[asset].iloc[-2]
        delta = ((current_price - previous_price) / previous_price) * 100
        
        # Formatação especial para o câmbio
        fmt = "R$ {:.2f}" if "BRL" in asset else "$ {:.2f}"
        cols[i].metric(label=asset, value=fmt.format(current_price), delta=f"{delta:.2f}%")

    st.markdown("---")

    # --- SECTION 2: PERFORMANCE & VOLATILITY ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Comparative Performance (Base 100)")
        dados_normalizados = (dados_limpos / dados_limpos.iloc[0]) * 100
        st.line_chart(dados_normalizados, height=400)

    with col_right:
        st.subheader("⚡ Risk (Daily Volatility)")
        # Calculando a volatilidade (Desvio padrão dos retornos)
        volatilidade = dados_limpos.pct_change().std() * 100
        st.bar_chart(volatilidade)

    st.markdown("---")

    # --- SECTION 3: RAW DATA & EXPORT ---
    st.subheader("📥 Data Inspection & Export")
    tab1, tab2 = st.tabs(["Closing Prices", "Daily Returns (%)"])
    
    with tab1:
        st.dataframe(dados_limpos, use_container_width=True)
        # Botão de Download
        csv = dados_limpos.to_csv().encode('utf-8')
        st.download_button(label="Download Prices as CSV", data=csv, file_name='market_prices.csv', mime='text/csv')

    with tab2:
        retornos = dados_limpos.pct_change().dropna() * 100
        st.dataframe(retornos.style.format("{:.2f}%"), use_container_width=True)

st.markdown("---")
st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data by Yahoo Finance API")
