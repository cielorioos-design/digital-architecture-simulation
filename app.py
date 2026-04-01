import streamlit as st
import time

st.set_page_config(page_title="Digital Architecture Simulation", layout="wide")

# -----------------------------
# STYLES
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.subtle {
    color: #5f6368;
    margin-bottom: 1.2rem;
}
.node {
    border-radius: 20px;
    padding: 20px 18px;
    text-align: center;
    font-weight: 700;
    min-height: 120px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    border: 2px solid transparent;
}
.device {
    background: linear-gradient(180deg, #f8f9ff, #eef3ff);
}
.edge {
    background: linear-gradient(180deg, #eefaf4, #e1f5ea);
}
.middleware {
    background: linear-gradient(180deg, #fff6ea, #fff0d6);
}
.cloud {
    background: linear-gradient(180deg, #f3f0ff, #ece7ff);
}
.active {
    border: 2px solid #6c63ff;
    transform: scale(1.01);
}
.packet {
    border-radius: 16px;
    padding: 14px 16px;
    background: white;
    border-left: 6px solid #6c63ff;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin: 8px 0;
    font-family: monospace;
    font-size: 0.92rem;
    white-space: pre-wrap;
}
.raw {
    border-left-color: #ff8a00;
}
.edgepkt {
    border-left-color: #00a86b;
}
midpkt {
    border-left-color: #0084ff;
}
.cloudpkt {
    border-left-color: #7c4dff;
}
.chip {
    display: inline-block;
    background: #eef1ff;
    color: #334;
    border-radius: 999px;
    padding: 5px 10px;
    margin: 4px 6px 4px 0;
    font-size: 0.82rem;
    font-weight: 600;
}
.arrowline {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    color: #6c63ff;
    margin: 10px 0;
}
.stage-box {
    background: #f9fafb;
    border: 1px solid #eceff3;
    border-radius: 16px;
    padding: 16px;
    margin-top: 10px;
}
.good {
    background: #edf8f1;
    border-left: 5px solid #00a86b;
    padding: 12px 14px;
    border-radius: 12px;
}
.note {
    background: #eef5ff;
    border-left: 5px solid #4a90e2;
    padding: 12px 14px;
    border-radius: 12px;
}
.small {
    font-size: 0.9rem;
    color: #5f6368;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Digital Architecture & Data Flow Simulation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">Visual simulation of how raw device data is generated, transformed at the edge, and passed through the architecture.</div>', unsafe_allow_html=True)

left, right = st.columns([1,1])
with left:
    play = st.button("▶ Play simulation", use_container_width=True)
with right:
    manual_step = st.slider("Or inspect a specific stage", 0, 5, 0)

# -----------------------------
# DATA
# -----------------------------
pv_raw = """PV_01 | Modbus
power_w: 3000
voltage_v: 230.4
frequency_hz: 49.85
status: producing"""

ev_raw = """EV_01 | OCPP
power_w: 3600
charging_status: charging
session_state: active"""

hp_raw = """HP_01 | Modbus
power_w: 1800
flow_temp_c: 42.3
status: heating"""

edge_packet = """EDGE GATEWAY OUTPUT
timestamp: 2026-03-20 12:00:00
gateway_id: EDGE_01
source_protocols: [Modbus, OCPP]
message_type: Unified edge message
forward_protocol: Prepared for MQTT transmission
control_action: No action"""

middleware_packet = """MIDDLEWARE OUTPUT
normalized_format: JSON
device_count: 3
pv_generation_w: 3000
total_demand_w: 5400
net_balance_w: -2400
operating_state: Grid import required"""

cloud_packet = """CLOUD VIEW
storage: time-series + historical records
analytics: demand/generation monitoring
status: data received successfully"""

control_packet = """CONTROL PATH
current scenario: no local control action
reason: edge monitoring, preprocessing, and forwarding only"""

stage_text = {
    0: "Stage 0 — Devices generate raw telemetry using their own protocols.",
    1: "Stage 1 — Raw packets are collected by the edge gateway.",
    2: "Stage 2 — The edge validates, timestamps, and preprocesses the data.",
    3: "Stage 3 — The edge prepares a unified MQTT-ready message for forwarding.",
    4: "Stage 4 — Middleware normalizes and aggregates the incoming data.",
    5: "Stage 5 — The cloud receives the processed data and the feedback path is available."
}

# -----------------------------
# RENDER FUNCTION
# -----------------------------
def render(stage):
    st.markdown(f'<div class="note"><strong>{stage_text[stage]}</strong></div>', unsafe_allow_html=True)

    # Top architecture row
    c1, c2, c3 = st.columns(3)
    with c1:
        cls = "node device active" if stage == 0 else "node device"
        st.markdown(f'<div class="{cls}">☀️ Solar PV<br><div class="small">Modbus • 3000 W</div></div>', unsafe_allow_html=True)
    with c2:
        cls = "node device active" if stage == 0 else "node device"
        st.markdown(f'<div class="{cls}">🚗 EV Charger<br><div class="small">OCPP • 3600 W</div></div>', unsafe_allow_html=True)
    with c3:
        cls = "node device active" if stage == 0 else "node device"
        st.markdown(f'<div class="{cls}">🔥 Heat Pump<br><div class="small">Modbus • 1800 W</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="arrowline">⬇</div>', unsafe_allow_html=True)

    cls = "node edge active" if stage in [1,2,3] else "node edge"
    st.markdown(f'<div class="{cls}">⚙️ Edge Gateway<br><div class="small">Preprocessing • Validation • Timestamp • Protocol preparation</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="arrowline">⬇ MQTT-ready</div>', unsafe_allow_html=True)

    cls = "node middleware active" if stage == 4 else "node middleware"
    st.markdown(f'<div class="{cls}">🧠 Middleware<br><div class="small">Normalization • Aggregation • Preparation for upper layers</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="arrowline">⬇</div>', unsafe_allow_html=True)

    cls = "node cloud active" if stage == 5 else "node cloud"
    st.markdown(f'<div class="{cls}">☁️ Cloud / ESBN-facing stages<br><div class="small">Storage • Analytics • Later protocol translation</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Inside view
    st.subheader("Inside View: Data Transformation")

    colA, colB = st.columns([1.1, 1])

    with colA:
        st.markdown('<div class="stage-box"><strong>Raw Device Packets</strong></div>', unsafe_allow_html=True)
        if stage >= 0:
            st.markdown(f'<div class="packet raw">{pv_raw}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="packet raw">{ev_raw}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="packet raw">{hp_raw}</div>', unsafe_allow_html=True)

    with colB:
        if stage >= 1:
            st.markdown('<div class="stage-box"><strong>Edge Processing View</strong></div>', unsafe_allow_html=True)
            st.markdown('<span class="chip">Data received</span><span class="chip">Source protocols identified</span>', unsafe_allow_html=True)
        if stage >= 2:
            st.markdown('<span class="chip">Validation: OK</span><span class="chip">Timestamp added</span><span class="chip">No action</span>', unsafe_allow_html=True)
        if stage >= 3:
            st.markdown(f'<div class="packet edgepkt">{edge_packet}</div>', unsafe_allow_html=True)
        if stage >= 4:
            st.markdown(f'<div class="packet edgepkt">{middleware_packet}</div>', unsafe_allow_html=True)
        if stage >= 5:
            st.markdown(f'<div class="packet edgepkt">{cloud_packet}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="packet edgepkt">{control_packet}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Explain stage outputs
    if stage >= 4:
        st.markdown(
            '<div class="good"><strong>Key interpretation:</strong> '
            'PV generation is 3000 W, total demand is 5400 W, so net balance is -2400 W. '
            'This means local demand exceeds local generation, so grid import is required.</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="small">Note: This simulation shows the logical processing of the architecture. '
        'TLS and IEEE 2030.5 are handled in later communication stages, not fully implemented here.</div>',
        unsafe_allow_html=True
    )

# -----------------------------
# DISPLAY
# -----------------------------
placeholder = st.empty()

if play:
    for s in range(0, 6):
        with placeholder.container():
            render(s)
        time.sleep(1.2)
else:
    with placeholder.container():
        render(manual_step)
