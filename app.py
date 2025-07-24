# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
import folium
from streamlit_folium import folium_static
import numpy as np

st.set_page_config(page_title="EVsync - Charging Demand Forecast", layout="wide")
st.title("⚡ EVsync: Predicting EV Growth & Charging Demand")

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/akshat-duggal/EVsync/refs/heads/main/forecast.csv")

# Preprocess data
df["Model Year"] = pd.to_datetime(df["Model Year"], format="%Y", errors='coerce')
df = df.dropna(subset=["Model Year"])
df["month"] = df["Model Year"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("month").size().reset_index(name="ev_count")

# Prophet modeling
df_prophet = monthly.rename(columns={"month": "ds", "ev_count": "y"})
m = Prophet()
m.fit(df_prophet)
future = m.make_future_dataframe(periods=60, freq="M")
forecast = m.predict(future)
forecast["estimated_charging_sessions"] = forecast["yhat"] * 1.5

# Interactive Future Explorer (Feature A)
st.sidebar.header("🔮 Explore Future Demand")
year_choice = st.sidebar.selectbox("Select Year to Forecast:", list(range(2024, 2031)))

selected_date = f"{year_choice}-12-01"
year_data = forecast[forecast['ds'] == selected_date]

if not year_data.empty:
    st.subheader(f"📅 Forecast for {year_choice}")
    st.metric("🔌 Estimated Charging Sessions", f"{int(year_data['estimated_charging_sessions'].values[0]):,}")
    st.metric("🚗 Predicted EVs", f"{int(year_data['yhat'].values[0]):,}")

# Heatmap (Feature B - simplified)
st.subheader("📍 EV Infrastructure Heatmap")
map_data = df.groupby("County").size().reset_index(name="count")
map_data = map_data.sort_values(by="count", ascending=False).head(10)
st.bar_chart(map_data.set_index("County"))

# Seasonal Demand Spike Detector (Feature D)
st.subheader("🌡️ Seasonal Demand Spike Detector")
fig_season = m.plot_seasonality(forecast, name='yearly')
st.pyplot(fig_season)

# Policy Simulation Slider (Feature F)
st.sidebar.header("👥 Policy Simulation")
adoption_increase = st.sidebar.slider("Govt. EV Adoption Boost (%)", 0, 50, 0, step=5)
charging_expansion = st.sidebar.slider("Private Charging Expansion (%)", 0, 50, 0, step=5)

policy_multiplier = 1 + ((adoption_increase + charging_expansion) / 100)
forecast["policy_adjusted_charging_sessions"] = forecast["estimated_charging_sessions"] * policy_multiplier

if not year_data.empty:
    policy_sessions = forecast[forecast['ds'] == selected_date]['policy_adjusted_charging_sessions'].values[0]
    st.metric("🧮 Policy-Adjusted Charging Sessions", f"{int(policy_sessions):,}")

# Forecast chart
st.subheader("📈 Forecasted EV Growth")
fig = px.line(forecast, x='ds', y='yhat', title="Projected EV Count Over Time")
st.plotly_chart(fig, use_container_width=True)

# Charging demand chart
st.subheader("🔌 Forecasted Charging Sessions (Adjusted)")
fig2 = px.line(forecast, x='ds', y='policy_adjusted_charging_sessions', title="Charging Sessions with Policy Effects")
st.plotly_chart(fig2, use_container_width=True)
