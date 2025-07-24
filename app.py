import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Set page config
st.set_page_config(page_title="🔋 EV Forecast Dashboard", layout="wide")

# --- LOAD FORECAST DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/akshat-duggal/EVsync/refs/heads/main/forecast.csv"  # your GitHub raw link
    df = pd.read_csv(url)
    df['month'] = pd.to_datetime(df['month'])
    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("🔧 Controls")
selected_year = st.sidebar.slider("Choose a Year", 2023, 2030, 2025)

# Policy Simulation
st.sidebar.subheader("🎯 Policy Simulation")
gov_subsidy = st.sidebar.slider("Govt EV Incentives (%)", 0, 30, 0, step=5)
private_expansion = st.sidebar.slider("Private Charging Expansion (%)", 0, 30, 0, step=5)

# --- APPLY POLICY EFFECT ---
df['adjusted_forecast'] = df['Forecast'] * (1 + (gov_subsidy + private_expansion) / 100)

# --- FILTER BY YEAR ---
df['year'] = df['month'].dt.year
future_df = df[df['year'] == selected_year]

# --- MAIN HEADER ---
st.title("🔮 EV Forecasting & Charging Demand Dashboard")
st.markdown("Forecasting electric vehicle adoption and infrastructure needs with interactive policy simulation.")

# --- SECTION A: Future Explorer ---
st.subheader(f"📊 Projected EV Stats for {selected_year}")
total_ev = int(future_df['adjusted_forecast'].sum())
charging_sessions = int(total_ev * 1.2)  # assume 1.2 sessions/month per EV

col1, col2 = st.columns(2)
col1.metric("🔌 Forecasted EVs", f"{total_ev:,}")
col2.metric("⚡ Expected Charging Sessions", f"{charging_sessions:,}")

# --- SECTION B: Heatmap Placeholder ---
st.subheader("🌍 County-Wise EV Adoption Heatmap")
st.info("📍 Your dataset currently lacks geographic columns (county/location). Heatmap unavailable until location data is added.")

# --- SECTION D: Seasonal Demand Insights ---
st.subheader("📅 Seasonal EV Adoption Trends")
monthly_avg = df.groupby(df['month'].dt.month)['adjusted_forecast'].mean().reset_index()
monthly_avg.columns = ['Month', 'Average Forecast']
fig2 = px.line(monthly_avg, x="Month", y="Average Forecast",
               title="Monthly Seasonality in EV Forecast",
               markers=True)
st.plotly_chart(fig2, use_container_width=True)

# --- SECTION F: Policy Simulation Summary ---
st.subheader("🧪 Policy Simulation Impact")
st.markdown(f"""
- 📈 Government subsidy impact: **+{gov_subsidy}%**
- 🏗️ Private charging network expansion: **+{private_expansion}%**
- 🔮 Total projected EVs in {selected_year}: **{total_ev:,}**
- ⚡ Estimated monthly charging sessions: **{charging_sessions:,}**
""")

# --- Show Data ---
with st.expander("🔍 View Forecast Dataset"):
    st.dataframe(df[['month', 'ev_count', 'Forecast', 'adjusted_forecast']])
