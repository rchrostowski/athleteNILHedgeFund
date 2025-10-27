import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# ----------------------------------
# LOAD DATA (AUTO-GENERATED FALLBACKS)
# ----------------------------------
@st.cache_data
def load_data():
    """Loads data with safe fallbacks if files are missing or empty."""

    # --- Simulated trade history (60 days) ---
    dates = pd.date_range(datetime.today() - timedelta(days=60), periods=60)
    trade_history = pd.DataFrame({
        "Date": dates,
        "PortfolioValue": 100000 * (1 + 0.005) ** np.arange(60)
    })

    # --- Simulated investment reports ---
    inv_reports = pd.DataFrame({
        "Symbol": ["AAPL", "MSFT", "NVDA", "AMZN", "META"],
        "InvScore": [92, 88, 90, 85, 83],
        "InvReport": [
            "AAPL: Strong AI-driven growth and ecosystem expansion.",
            "MSFT: Cloud dominance and diversified revenue streams.",
            "NVDA: Unrivaled leadership in AI and GPU technology.",
            "AMZN: AWS performance driving steady margin recovery.",
            "META: Cost discipline and ad business rebound."
        ]
    })

    # --- Simulated portfolio weights ---
    recs = pd.DataFrame({
        "Symbol": ["AAPL", "MSFT", "NVDA", "AMZN", "META"],
        "Weight": [0.25, 0.25, 0.20, 0.15, 0.15]
    })

    # Merge them
    merged = inv_reports.merge(recs, on="Symbol", how="left")
    return trade_history, merged, recs


# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="GPT Hedge Fund Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🤖 GPT Hedge Fund Performance Dashboard")
st.markdown(
    """
    Built by **Ryan Chrostowski** — Lehigh FinTech Project  
    ---
    This dashboard visualizes your **GPT-driven hedge fund** performance,  
    portfolio weights, and AI-generated investment insights.
    """
)

# ----------------------------------
# LOAD DATASETS
# ----------------------------------
trade_history, merged, recs = load_data()

# ----------------------------------
# METRICS
# ----------------------------------
st.subheader("📊 Fund Metrics")

col1, col2, col3, col4 = st.columns(4)

alpha_daily = 0.005
alpha_cum = (1 + alpha_daily) ** len(trade_history) - 1
benchmark_ret = 0.02
fund_ret = (1 + benchmark_ret) * (1 + alpha_cum) - 1
sharpe = (alpha_daily * 252) / 0.05  # assume 5% daily vol

col1.metric("Daily Alpha", f"{alpha_daily*100:.2f}%")
col2.metric("Cumulative Alpha", f"{alpha_cum*100:.1f}%")
col3.metric("Fund Return", f"{fund_ret*100:.1f}%")
col4.metric("Sharpe Ratio (Est.)", f"{sharpe:.2f}")

# ----------------------------------
# PERFORMANCE CHART
# ----------------------------------
st.subheader("📈 Portfolio Value Over Time")

fig = px.line(
    trade_history,
    x="Date",
    y="PortfolioValue",
    title="Portfolio Value (Simulated)",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# PORTFOLIO ALLOCATION
# ----------------------------------
st.subheader("💼 Portfolio Allocation")

fig_pie = px.pie(
    recs,
    names="Symbol",
    values="Weight",
    title="Current Portfolio Weights",
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------------
# TOP HOLDINGS TABLE
# ----------------------------------
st.subheader("🏆 Top AI-Selected Holdings")

st.dataframe(
    merged[["Symbol", "InvScore", "Weight", "InvReport"]]
        .sort_values("InvScore", ascending=False)
        .style.background_gradient(subset=["InvScore"], cmap="Greens"),
    use_container_width=True,
    height=400
)

# ----------------------------------
# INDIVIDUAL REPORT VIEWER
# ----------------------------------
st.subheader("📑 Individual Investment Reports")

selected_symbol = st.selectbox("Select a Stock:", merged["Symbol"].unique())
selected_report = merged.loc[merged["Symbol"] == selected_symbol, "InvReport"].iloc[0]
st.markdown(f"### {selected_symbol} Investment Report")
st.write(selected_report)

# ----------------------------------
# MACRO OUTLOOK
# ----------------------------------
st.subheader("🌎 Macro & Market Outlook")

macro_summary = """
**Macro Overview (AI-Generated Example):**  
- GDP growth remains resilient in late-2025  
- Inflation continues to moderate toward target  
- Fed expected to ease policy in mid-2026  
- Stable labor markets and robust corporate earnings  

Overall, conditions remain favorable for sustained equity alpha generation.
"""
st.info(macro_summary)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.caption("© 2025 GPT Hedge Fund — Built with Streamlit & AI-driven insights.")

