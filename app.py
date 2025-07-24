
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🔌 EV Charging Demand Forecast", layout="wide")

st.title("🔋 EV Charging Demand Forecast (2024–2030)")
st.markdown("Forecasting EV adoption & charging needs using real-world trends 🚗⚡")

# Load the forecast data
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/akshat-duggal/EVsync/refs/heads/main/forecast.csv")
    df['ds'] = pd.to_datetime(df['ds'])
    df.rename(columns={'ds': 'month', 'yhat': 'ev_count'}, inplace=True)
    df['estimated_charging_sessions'] = df['ev_count'] * 1.5
    return df

df = load_data()

# Sidebar – Year selector
st.sidebar.header("🔮 Explore Future Demand")
year_choice = st.sidebar.selectbox("Select Year to Forecast:", list(range(2024, 2031)))

selected_date = f"{year_choice}-12-01"
year_data = df[df['month'] == selected_date]

if not year_data.empty:
    st.subheader(f"📅 Forecast for {year_choice}")
    col1, col2 = st.columns(2)
    col1.metric("🚗 Predicted EVs", f"{int(year_data['ev_count'].values[0]):,}")
    col2.metric("🔌 Estimated Charging Sessions", f"{int(year_data['estimated_charging_sessions'].values[0]):,}")

# A. Line chart of EV growth
st.subheader("📈 EV Growth Forecast")
fig1 = px.line(df, x='month', y='ev_count', title="Projected Number of EVs Over Time", markers=True)
fig1.update_traces(line=dict(color="green"))
st.plotly_chart(fig1, use_container_width=True)

# B. Charging demand chart
st.subheader("⚡ Forecasted Charging Demand")
fig2 = px.line(df, x='month', y='estimated_charging_sessions', title="Estimated Charging Sessions Over Time", markers=True)
fig2.update_traces(line=dict(color="orange"))
st.plotly_chart(fig2, use_container_width=True)

# D. Seasonal Demand Spike Detector (simple display)
st.subheader("📊 Seasonal Trends")
df['month_name'] = df['month'].dt.strftime('%b')
monthly_avg = df.groupby('month_name')['estimated_charging_sessions'].mean().reindex([
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])
st.bar_chart(monthly_avg)

# F. Policy Simulation (Subsidy Slider)
st.subheader("⚙️ Policy Simulation – Boost EV Adoption")
subsidy = st.slider("Simulate % Increase in EV Adoption", 0, 50, 0, step=5)
simulated_df = df.copy()
simulated_df['ev_count'] *= (1 + subsidy / 100)
simulated_df['estimated_charging_sessions'] = simulated_df['ev_count'] * 1.5

fig3 = px.line(simulated_df, x='month', y='ev_count', title=f"EV Adoption with {subsidy}% Subsidy", markers=True)
fig3.update_traces(line=dict(color="purple"))
st.plotly_chart(fig3, use_container_width=True)
