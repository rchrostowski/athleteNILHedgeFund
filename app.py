import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    """Loads trade history, investment reports, and portfolio recommendations."""
    # --- Trade History ---
    try:
        trade_history = pd.read_excel("trade_history.xlsx", engine="openpyxl")
    except FileNotFoundError:
        st.warning("⚠️ trade_history.xlsx not found — loading sample performance data.")
        dates = pd.date_range(datetime.today() - timedelta(days=60), periods=60)
        trade_history = pd.DataFrame({
            "Date": dates,
            "PortfolioValue": 100000 * (1 + 0.005) ** np.arange(60)
        })
    except ValueError:
        st.error("❌ trade_history.xlsx is not a valid Excel file. Please re-save as .xlsx format.")
        raise

    # --- Investment Reports ---
    try:
        inv_reports = pd.read_csv("stock_investment_reports.csv")
    except FileNotFoundError:
        st.warning("⚠️ stock_investment_reports.csv not found — using demo data.")
        inv_reports = pd.DataFrame({
            "Symbol": ["AAPL", "MSFT", "NVDA", "AMZN", "META"],
            "InvScore": [92, 88, 85, 83, 81],
            "InvReport": ["Strong momentum and AI-driven growth."] * 5
        })

    # --- Recommendations ---
    try:
        recs = pd.read_csv("recommendations.csv")
    except FileNotFoundError:
        st.warning("⚠️ recommendations.csv not found — using equal-weight portfolio.")
        recs = pd.DataFrame({
            "Symbol": ["AAPL", "MSFT", "NVDA", "AMZN", "META"],
            "Weight": [0.2, 0.2, 0.2, 0.2, 0.2]
        })

    # Merge datasets
    merged = inv_reports.merge(recs, on="Symbol", how="left")
    merged["Weight"] = merged["Weight"].fillna(0)
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
    This dashboard tracks your **GPT Hedge Fund’s daily alpha, portfolio composition,**  
    and AI-generated investment reports.
    """
)

# ----------------------------------
# LOAD DATASETS
# ----------------------------------
trade_history, merged, recs = load_data()

# ----------------------------------
# METRICS SECTION
# ----------------------------------
st.subheader("📊 Fund Metrics")

col1, col2, col3, col4 = st.columns(4)

# Example metrics — replace with real ones when connected to live performance
alpha_daily = 0.005  # 0.5% daily alpha
alpha_cum = (1 + alpha_daily) ** len(trade_history) - 1
benchmark_ret = 0.02  # hypothetical S&P return over period
fund_ret = (1 + benchmark_ret) * (1 + alpha_cum) - 1
sharpe = (alpha_daily * 252) / 0.05  # assume 5% daily vol

col1.metric("Daily Alpha", f"{alpha_daily*100:.2f}%")
col2.metric("Cumulative Alpha", f"{alpha_cum*100:.1f}%")
col3.metric("Total Fund Return", f"{fund_ret*100:.1f}%")
col4.metric("Sharpe Ratio (Est.)", f"{sharpe:.2f}")

# ----------------------------------
# PERFORMANCE CHART
# ----------------------------------
st.subheader("📈 Portfolio Value Over Time")

if "Date" in trade_history.columns and "PortfolioValue" in trade_history.columns:
    fig = px.line(
        trade_history,
        x="Date",
        y="PortfolioValue",
        title="Portfolio Value (Simulated)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Upload a file with 'Date' and 'PortfolioValue' columns to see performance trends.")

# ----------------------------------
# PORTFOLIO WEIGHTS
# ----------------------------------
st.subheader("💼 Portfolio Weight Distribution")

if not recs.empty and "Symbol" in recs.columns and "Weight" in recs.columns:
    fig_pie = px.pie(
        recs,
        names="Symbol",
        values="Weight",
        title="Current Portfolio Allocation",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No weight data available.")

# ----------------------------------
# TOP HOLDINGS TABLE
# ----------------------------------
st.subheader("🏆 Top AI-Selected Holdings")

if "InvScore" in merged.columns:
    top_df = merged.sort_values("InvScore", ascending=False).head(10)
    st.dataframe(
        top_df[["Symbol", "InvScore", "Weight", "InvReport"]].style.background_gradient(
            subset=["InvScore"], cmap="Greens"
        ),
        use_container_width=True,
        height=400
    )
else:
    st.info("Investment score data not available.")

# ----------------------------------
# INDIVIDUAL REPORT VIEWER
# ----------------------------------
st.subheader("📑 Individual Investment Reports")

if "Symbol" in merged.columns:
    selected_symbol = st.selectbox("Select a Stock:", merged["Symbol"].unique())
    selected_report = merged.loc[merged["Symbol"] == selected_symbol, "InvReport"].iloc[0]
    st.markdown(f"### {selected_symbol} Investment Report")
    st.write(selected_report)
else:
    st.info("No investment reports to display.")

# ----------------------------------
# MACRO OUTLOOK (Optional Text Block)
# ----------------------------------
st.subheader("🌎 Macro & Market Outlook")

macro_summary = """
**Market Summary (AI Generated):**
- GDP growth remains resilient in 2025  
- Inflation continues to moderate  
- Fed policy expected to turn accommodative mid-2025  
- Labor market stable; volatility low  

Overall, macro conditions are supportive for equity risk-taking and alpha generation.
"""
st.info(macro_summary)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.caption("© 2025 GPT Hedge Fund — Built with Streamlit and AI-powered insights.")

