import streamlit as st
import pandas as pd

st.set_page_config(page_title="Digital Architecture Simulation", layout="wide")

st.title("⚡ Digital Architecture & Data Flow Simulation")

st.markdown("Simulation of data flow from DER devices through Edge, Middleware, and Cloud layers.")

# -----------------------------
# RAW DEVICE DATA
# -----------------------------
st.subheader("1. Device Layer - Raw Telemetry")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ☀️ Solar PV")
    st.metric("Power", "3000 W")
    st.write("Protocol: Modbus")
    st.write("Voltage: 230.4 V")
    st.write("Frequency: 49.85 Hz")
    st.write("Status: producing")

with col2:
    st.markdown("### 🚗 EV Charger")
    st.metric("Power", "3600 W")
    st.write("Protocol: OCPP")
    st.write("Status: charging")

with col3:
    st.markdown("### 🔥 Heat Pump")
    st.metric("Power", "1800 W")
    st.write("Protocol: Modbus")
    st.write("Flow Temp: 42.3 °C")
    st.write("Status: heating")

# -----------------------------
# EDGE LAYER
# -----------------------------
st.subheader("2. Edge Layer Operation")

st.info("Edge gateway receives data, validates it, timestamps it, and prepares it for MQTT transmission.")

edge_data = pd.DataFrame([
    ["PV_01", "Modbus", "Unified format", "MQTT-ready", "No action"],
    ["EV_01", "OCPP", "Unified format", "MQTT-ready", "No action"],
    ["HP_01", "Modbus", "Unified format", "MQTT-ready", "No action"]
], columns=["Device", "Protocol", "Processed Format", "Forwarding", "Control Action"])

st.dataframe(edge_data)

# -----------------------------
# SYSTEM SUMMARY
# -----------------------------
st.subheader("3. System Summary")

pv = 3000
demand = 3600 + 1800
net = pv - demand

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("PV Generation", f"{pv} W")

with col2:
    st.metric("Total Demand", f"{demand} W")

with col3:
    st.metric("Net Balance", f"{net} W")

if net < 0:
    st.error("Grid import required")
else:
    st.success("Surplus energy available")

# -----------------------------
# CLOUD / MIDDLEWARE
# -----------------------------
st.subheader("4. Middleware & Cloud")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Middleware")
    st.write("- Data validation")
    st.write("- Data normalization")
    st.write("- Aggregation")

with col2:
    st.markdown("### Cloud / ESBN")
    st.write("- Data storage")
    st.write("- Analytics & forecasting")
    st.write("- IEEE 2030.5 happens here later")

st.markdown("---")
st.caption("Edge role: Monitoring, preprocessing, and forwarding")
