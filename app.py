import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuração inicial da página (Aba do navegador)
st.set_page_config(page_title="Market Intelligence", layout="wide")

# 2. Títulos do seu Web App
st.title("📈 Financial Market Intelligence Dashboard")
st.markdown("Painel automatizado de ETL para Commodities e Câmbio.")
st.markdown("---")

# 3. Criando um Menu Lateral (Sidebar) para o usuário interagir
st.sidebar.header("⚙️ Parâmetros da Análise")
dias_historico = st.sidebar.slider("Selecione o período (Dias):", min_value=7, max_value=365, value=30)

# 4. Função inteligente para buscar dados (com Cache para não travar o site)
@st.cache_data
def carregar_dados(dias):
    tickers = ["CL=F", "GC=F", "ZC=F", "BRL=X"]
    end_date = datetime.today()
    start_date = end_date - timedelta(days=dias)
    
    df = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', progress=False)
    
    close_prices = pd.DataFrame()
    for ticker in tickers:
        if ticker in df.columns.levels[0]:
            close_prices[ticker] = df[ticker]['Close']
            
    close_prices.columns = ["Crude Oil (USD)", "Gold (USD)", "Corn (USD)", "USD/BRL"]
    
    # Limpando os buracos de feriados (ffill)
    return close_prices.ffill().dropna()

# 5. Executando a extração com base no menu lateral
st.write(f"🔄 Extraindo e limpando dados dos últimos **{dias_historico} dias** via Yahoo Finance API...")
dados_limpos = carregar_dados(dias_historico)

# 6. Dividindo a tela em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Tabela de Preços (Raw Data)")
    # O Streamlit cria uma tabela linda e interativa sozinho
    st.dataframe(dados_limpos, use_container_width=True)

with col2:
    st.subheader("📈 Retorno Diário (%)")
    retornos = dados_limpos.pct_change().dropna() * 100
    st.dataframe(retornos.style.format("{:.2f}%"), use_container_width=True)

# 7. Gráfico Interativo Base 100 na tela principal
st.markdown("---")
st.subheader("📊 Performance Comparativa (Base 100)")
st.markdown("Se você tivesse investido $100 em cada ativo no início do período, quanto teria hoje?")

dados_normalizados = (dados_limpos / dados_limpos.iloc[0]) * 100
# O Streamlit gera um gráfico interativo (dá pra passar o mouse por cima!)
st.line_chart(dados_normalizados, height=400)