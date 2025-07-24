# streamlit_app/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---- CONFIG ----
st.set_page_config(page_title="EV Demand Forecast", layout="wide")

# ---- TITLE ----
st.title("🔋 ChargeCast: EV Adoption & Charging Demand Forecast")

# ---- LOAD FORECAST DATA ----
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/your-username/ev-demand-forecast/main/forecast.csv"  # replace!
    df = pd.read_csv(url, parse_dates=['ds'])
    return df

df = load_data()

# ---- DATE FILTER ----
min_date = df['ds'].min().date()
max_date = df['ds'].max().date()
start_date, end_date = st.slider("Select forecast range:",
                                 min_value=min_date,
                                 max_value=max_date,
                                 value=(min_date, max_date),
                                 format="YYYY-MM")

filtered = df[(df['ds'].dt.date >= start_date) & (df['ds'].dt.date <= end_date)]

# ---- METRICS ----
latest_ev = int(filtered['yhat'].iloc[-1])
latest_charging = int(filtered['charging_sessions'].iloc[-1])
st.metric("📈 Forecasted EVs", f"{latest_ev:,}")
st.metric("⚡ Charging Sessions", f"{latest_charging:,} / month")

# ---- LINE PLOT ----
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered['ds'], filtered['yhat'], label="Forecasted EVs", color='green')
ax.plot(filtered['ds'], filtered['charging_sessions'], label="Charging Demand", color='blue', linestyle='--')
ax.set_title("EV Adoption and Charging Demand Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Count")
ax.grid(True)
ax.legend()
st.pyplot(fig)
