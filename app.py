import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Intelligence", layout="wide")

st.title("📈 Financial Market Intelligence Dashboard")
st.markdown("Painel automatizado de ETL para Commodities e Câmbio.")
st.markdown("---")

st.sidebar.header("⚙️ Parâmetros da Análise")
dias_historico = st.sidebar.slider("Selecione o período (Dias):", min_value=7, max_value=365, value=30)

@st.cache_data(ttl=3600)
def carregar_dados(dias):
    tickers = ["CL=F", "GC=F", "ZC=F", "BRL=X"]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=dias)
    
    # Download direto e robusto (funciona com a versão mais nova do yfinance)
    df = yf.download(tickers, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        return pd.DataFrame()
        
    # Isola os preços de fechamento (Close)
    close_prices = df['Close'].copy()
    
    # Garante que temos as 4 colunas na ordem correta
    for ticker in tickers:
        if ticker not in close_prices.columns:
            close_prices[ticker] = None
            
    close_prices = close_prices[tickers]
    close_prices.columns = ["Crude Oil (USD)", "Gold (USD)", "Corn (USD)", "USD/BRL"]
    
    # Limpa os buracos (ffill)
    return close_prices.ffill().dropna()

st.write(f"🔄 Extraindo dados dos últimos **{dias_historico} dias** via Yahoo Finance API...")

# Executa a extração
dados_limpos = carregar_dados(dias_historico)

# O Escudo de Proteção: Só faz os cálculos se os dados existirem
if dados_limpos.empty:
    st.error("⚠️ Os dados retornaram vazios. O Yahoo Finance pode estar passando por uma instabilidade momentânea ou o mercado está fechado. Tente alterar os dias no menu lateral.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Tabela de Preços (Raw Data)")
        st.dataframe(dados_limpos, use_container_width=True)

    with col2:
        st.subheader("📈 Retorno Diário (%)")
        retornos = dados_limpos.pct_change().dropna() * 100
        st.dataframe(retornos.style.format("{:.2f}%"), use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Performance Comparativa (Base 100)")
    st.markdown("Se você tivesse investido $100 em cada ativo no início do período, quanto teria hoje?")

    # Agora o cálculo matemático está seguro!
    dados_normalizados = (dados_limpos / dados_limpos.iloc[0]) * 100
    st.line_chart(dados_normalizados, height=400)
