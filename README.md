# 🏛️ Alpha Market Intelligence Pro
### 🔴 **Live Web App:** [Access the Interactive Dashboard](https://fernando-market-data.streamlit.app)

## 🎯 Project Overview
In high-stakes financial environments, the ability to transform raw market data into actionable insights is the true "Alpha". This project is a professional **Quantitative ETL Pipeline & Analytics Dashboard** designed to monitor global assets in real-time.

Instead of static reports, this tool provides a dynamic interface for analyzing price trends, correlations, and volatility, allowing stakeholders to make data-driven decisions regarding Commodities and FX markets.

### 📊 Assets Monitored (Real-Time API)
- **Crude Oil (WTI):** Energy sector benchmark.
- **Gold:** Global safe-haven and inflation hedge.
- **Corn:** Agricultural supply chain indicator.
- **USD/BRL:** Emerging markets currency risk.

---

## 🚀 Technical Architecture & Features

### 1. Data Engineering (ETL)
- **Extraction:** Automated ingestion via `yfinance` API, eliminating manual data entry.
- **Transformation:** Robust cleaning pipeline using `pandas`. It handles market holidays and time-zone misalignments using **Forward Fill (ffill)** logic to ensure time-series integrity.
- **Loading:** Data is processed in-memory and cached using `@st.cache_data` to optimize performance and API limits.

### 2. Quantitative Analytics
- **Normalized Performance (Base 100):** Mathematical standardization to compare asset growth regardless of their nominal price differences.
- **Risk Metrics:** Calculation of **Annualized Volatility** (Std Dev * sqrt(252)) to quantify market risk.
- **Inter-asset Correlation:** A dynamic **Correlation Matrix** with heatmapping to identify how assets move in relation to each other (Diversification Analysis).

### 3. Professional UI/UX (Streamlit)
- **Real-Time KPIs:** Custom-styled metric cards showing current price and daily delta.
- **Interactive Timeframes:** Users can adjust the analysis window from 7 to 365 days.
- **Data Portability:** Integrated "Export to CSV" feature for downstream analysis in Excel or BI tools.

---

## 🛠️ Tech Stack
- **Language:** Python 3.13+
- **Framework:** Streamlit (Web UI)
- **Data Science:** Pandas, NumPy (Vectorized calculations)
- **Finance API:** yfinance
- **Styling:** Custom CSS for high-contrast UI components

---

## ⚙️ Quick Start (Run Locally)

To clone and run this application on your machine in one go, paste this into your terminal:

```bash
git clone [https://github.com/fernandogsloboda/financial-market-pipeline.git](https://github.com/fernandogsloboda/financial-market-pipeline.git) && cd financial-market-pipeline && pip install -r requirements.txt && streamlit run app.py
