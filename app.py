import streamlit as st
import time

st.set_page_config(layout="wide")

st.title("⚡ Digital Architecture Simulation")
st.markdown("Visual simulation of data flow across Edge, Middleware, and Cloud")

# -----------------------------
# STEP CONTROL
# -----------------------------
step = st.slider("Simulation Step", 1, 6, 1)

# -----------------------------
# STYLE (THIS MAKES IT CUTE)
# -----------------------------
st.markdown("""
<style>
.box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-weight: bold;
    margin: 10px;
    background-color: #f0f2f6;
}

.active {
    background-color: #d1ecff;
    border: 2px solid #3399ff;
}

.arrow {
    text-align: center;
    font-size: 30px;
}

.packet {
    width: 15px;
    height: 15px;
    background-color: #00cc66;
    border-radius: 50%;
    position: relative;
    animation: move 2s linear infinite;
}

@keyframes move {
    0% { left: 0px; }
    100% { left: 100px; }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DEVICE LAYER
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    cls = "box active" if step == 1 else "box"
    st.markdown(f'<div class="{cls}">☀️ Solar PV<br>3000W<br>Modbus</div>', unsafe_allow_html=True)

with col2:
    cls = "box active" if step == 1 else "box"
    st.markdown(f'<div class="{cls}">🚗 EV Charger<br>3600W<br>OCPP</div>', unsafe_allow_html=True)

with col3:
    cls = "box active" if step == 1 else "box"
    st.markdown(f'<div class="{cls}">🔥 Heat Pump<br>1800W<br>Modbus</div>', unsafe_allow_html=True)

# -----------------------------
# ARROW DOWN
# -----------------------------
if step >= 2:
    st.markdown('<div class="arrow">⬇️</div>', unsafe_allow_html=True)
    st.markdown('<div class="packet"></div>', unsafe_allow_html=True)

# -----------------------------
# EDGE LAYER
# -----------------------------
cls = "box active" if step == 2 else "box"
st.markdown(f'<div class="{cls}">⚙️ EDGE GATEWAY<br>Preprocessing • Validation • Timestamp</div>', unsafe_allow_html=True)

# -----------------------------
# EDGE → MIDDLEWARE
# -----------------------------
if step >= 3:
    st.markdown('<div class="arrow">⬇️ MQTT (TLS)</div>', unsafe_allow_html=True)
    st.markdown('<div class="packet"></div>', unsafe_allow_html=True)

# -----------------------------
# MIDDLEWARE
# -----------------------------
cls = "box active" if step == 3 else "box"
st.markdown(f'<div class="{cls}">🧠 MIDDLEWARE<br>Normalization • Aggregation</div>', unsafe_allow_html=True)

# -----------------------------
# MIDDLEWARE → CLOUD
# -----------------------------
if step >= 4:
    st.markdown('<div class="arrow">⬇️ HTTPS</div>', unsafe_allow_html=True)
    st.markdown('<div class="packet"></div>', unsafe_allow_html=True)

# -----------------------------
# CLOUD
# -----------------------------
cls = "box active" if step == 4 else "box"
st.markdown(f'<div class="{cls}">☁️ CLOUD<br>Analytics • Storage • Forecasting</div>', unsafe_allow_html=True)

# -----------------------------
# CONTROL SIGNAL BACK
# -----------------------------
if step >= 5:
    st.markdown('<div class="arrow">⬆️ Control Signal</div>', unsafe_allow_html=True)
    st.markdown('<div class="packet"></div>', unsafe_allow_html=True)

# -----------------------------
# FINAL STATE
# -----------------------------
if step == 6:
    st.success("System running: Edge monitoring, cloud optimizing, no local control action")

# -----------------------------
# EXPLANATION PANEL
# -----------------------------
st.markdown("---")

if step == 1:
    st.info("Devices generate raw telemetry using different protocols (Modbus, OCPP).")

elif step == 2:
    st.info("Edge receives data, validates it, timestamps it, and prepares it.")

elif step == 3:
    st.info("Data is converted to MQTT format and securely transmitted (TLS).")

elif step == 4:
    st.info("Middleware and cloud process the data for storage and analytics.")

elif step == 5:
    st.info("Cloud can send control signals back to the edge if needed.")

elif step == 6:
    st.info("In this scenario, edge performs monitoring and forwarding only (no control).")
