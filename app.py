import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Digital Architecture Simulation", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Digital Architecture Simulation</title>
<style>
    body {
        margin: 0;
        font-family: Inter, Arial, sans-serif;
        background: #f6f8fc;
        color: #1f2937;
    }

    .wrap {
        max-width: 1500px;
        margin: 0 auto;
        padding: 20px 24px 30px 24px;
    }

    .title {
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .subtitle {
        font-size: 18px;
        color: #64748b;
        margin-bottom: 18px;
    }

    .controls {
        display: flex;
        gap: 12px;
        margin-bottom: 18px;
        align-items: center;
    }

    button {
        border: none;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 16px;
        font-weight: 700;
        background: #6d5dfc;
        color: white;
        cursor: pointer;
        box-shadow: 0 6px 16px rgba(109,93,252,0.25);
    }

    button.secondary {
        background: #e8ecf8;
        color: #25324a;
        box-shadow: none;
    }

    .stage-indicator {
        display: inline-block;
        background: #e9f2ff;
        color: #2055b5;
        border-left: 5px solid #4f8df7;
        padding: 12px 14px;
        border-radius: 12px;
        font-weight: 700;
        margin-bottom: 18px;
        min-width: 360px;
    }

    .pipeline {
        display: grid;
        grid-template-columns: 1.3fr 0.2fr 1.3fr 0.2fr 1.3fr 0.2fr 1.3fr 0.2fr 1.3fr;
        gap: 10px;
        align-items: center;
        margin-bottom: 22px;
    }

    .layer {
        min-height: 145px;
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        border: 3px solid transparent;
        position: relative;
        overflow: hidden;
    }

    .layer.active {
        border-color: #6d5dfc;
        transform: translateY(-2px);
    }

    .devices { background: linear-gradient(180deg, #eef4ff, #e6efff); }
    .edge { background: linear-gradient(180deg, #eefcf5, #e3f8ea); }
    .transport { background: linear-gradient(180deg, #fff8ec, #ffefd4); }
    .middleware { background: linear-gradient(180deg, #fffaf0, #fff1dd); }
    .cloud { background: linear-gradient(180deg, #f3f0ff, #ece7ff); }
    .std { background: linear-gradient(180deg, #eef8ff, #e4f1ff); }
    .esbn { background: linear-gradient(180deg, #f2f7ff, #e8f0ff); }

    .layer-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .mini {
        color: #5f6b7a;
        font-size: 14px;
        font-weight: 700;
    }

    .node-list {
        margin-top: 12px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .device-card {
        background: rgba(255,255,255,0.72);
        border-radius: 16px;
        padding: 10px 12px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.6);
    }

    .device-name {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .device-meta {
        font-size: 14px;
        color: #4f5d6b;
        line-height: 1.4;
    }

    .arrow {
        text-align: center;
        font-size: 34px;
        font-weight: 900;
        color: #6d5dfc;
    }

    .packet-zone {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 8px;
    }

    .packet {
        border-radius: 18px;
        padding: 14px 16px;
        background: white;
        box-shadow: 0 10px 22px rgba(0,0,0,0.08);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 14px;
        line-height: 1.5;
        border-left: 8px solid #6d5dfc;
        white-space: pre-wrap;
        opacity: 0.18;
        transform: scale(0.98);
        transition: all 0.35s ease;
    }

    .packet.visible {
        opacity: 1;
        transform: scale(1);
    }

    .raw { border-left-color: #ff8a00; }
    .edgepkt { border-left-color: #00a86b; }
    .midpkt { border-left-color: #0284c7; }
    .cloudpkt { border-left-color: #7c3aed; }
    .stdpkt { border-left-color: #2563eb; }
    .ctrlpkt { border-left-color: #f59e0b; }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 14px;
    }

    .metric {
        background: rgba(255,255,255,0.84);
        border-radius: 18px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.06);
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 900;
    }

    .moving-area {
        margin-top: 18px;
        height: 76px;
        position: relative;
        border-radius: 18px;
        background: #ffffff;
        box-shadow: inset 0 0 0 1px #e9edf6;
        overflow: hidden;
    }

    .track {
        position: absolute;
        top: 36px;
        left: 24px;
        right: 24px;
        height: 4px;
        background: linear-gradient(90deg, #dbe5ff, #d8f6e7, #fff0cc, #e7dcff, #dbeafe);
        border-radius: 999px;
    }

    .packet-chip {
        position: absolute;
        top: 20px;
        left: 24px;
        padding: 8px 14px;
        border-radius: 999px;
        color: white;
        font-weight: 800;
        font-size: 13px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.16);
        opacity: 0;
    }

    .chip1 { background: #ff8a00; }
    .chip2 { background: #00a86b; }
    .chip3 { background: #0284c7; }
    .chip4 { background: #7c3aed; }
    .chip5 { background: #f59e0b; }

    .animate1 { animation: move1 1.2s linear forwards; opacity: 1; }
    .animate2 { animation: move2 1.2s linear forwards; opacity: 1; }
    .animate3 { animation: move3 1.2s linear forwards; opacity: 1; }
    .animate4 { animation: move4 1.2s linear forwards; opacity: 1; }
    .animate5 { animation: move5 1.2s linear forwards; opacity: 1; }

    @keyframes move1 { from { left: 2%; } to { left: 22%; } }
    @keyframes move2 { from { left: 22%; } to { left: 42%; } }
    @keyframes move3 { from { left: 42%; } to { left: 62%; } }
    @keyframes move4 { from { left: 62%; } to { left: 82%; } }
    @keyframes move5 { from { left: 82%; } to { left: 62%; } }

    .tiny-note {
        margin-top: 12px;
        color: #64748b;
        font-size: 13px;
        font-weight: 700;
    }
</style>
</head>
<body>
<div class="wrap">
    <div class="title">⚡ Digital Architecture & Data Flow Simulation</div>
    <div class="subtitle">End-to-end visual simulation of how DER data moves through the full architecture.</div>

    <div class="controls">
        <button onclick="playSimulation()">▶ Play simulation</button>
        <button class="secondary" onclick="setStage(0)">Stage 0</button>
        <button class="secondary" onclick="setStage(1)">1</button>
        <button class="secondary" onclick="setStage(2)">2</button>
        <button class="secondary" onclick="setStage(3)">3</button>
        <button class="secondary" onclick="setStage(4)">4</button>
        <button class="secondary" onclick="setStage(5)">5</button>
    </div>

    <div id="stageIndicator" class="stage-indicator">Stage 0 — Raw telemetry generation</div>

    <div class="pipeline">
        <div id="devicesLayer" class="layer devices active">
            <div class="layer-title">Devices</div>
            <div class="mini">Raw telemetry generation</div>
            <div class="node-list">
                <div class="device-card">
                    <div class="device-name">☀️ Solar PV</div>
                    <div class="device-meta">3000 W • 230.4 V • 49.85 Hz • Modbus</div>
                </div>
                <div class="device-card">
                    <div class="device-name">🚗 EV Charger</div>
                    <div class="device-meta">3600 W • charging • OCPP</div>
                </div>
                <div class="device-card">
                    <div class="device-name">🔥 Heat Pump</div>
                    <div class="device-meta">1800 W • 42.3 °C • Modbus</div>
                </div>
            </div>
        </div>

        <div class="arrow">➜</div>

        <div id="edgeLayer" class="layer edge">
            <div class="layer-title">Edge Gateway</div>
            <div class="mini">Validation • Timestamp • Preprocessing</div>
            <div class="metric-row">
                <div class="metric">
                    <div class="metric-label">Gateway ID</div>
                    <div class="metric-value">EDGE_01</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Data quality</div>
                    <div class="metric-value">OK</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Action</div>
                    <div class="metric-value">None</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Output</div>
                    <div class="metric-value">MQTT</div>
                </div>
            </div>
        </div>

        <div class="arrow">➜</div>

        <div id="middlewareLayer" class="layer middleware">
            <div class="layer-title">Middleware</div>
            <div class="mini">Normalization • Aggregation • JSON</div>
            <div class="metric-row">
                <div class="metric">
                    <div class="metric-label">PV generation</div>
                    <div class="metric-value">3000</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Demand</div>
                    <div class="metric-value">5400</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Net balance</div>
                    <div class="metric-value">-2400</div>
                </div>
                <div class="metric">
                    <div class="metric-label">State</div>
                    <div class="metric-value">Import</div>
                </div>
            </div>
        </div>

        <div class="arrow">➜</div>

        <div id="cloudLayer" class="layer cloud">
            <div class="layer-title">Cloud</div>
            <div class="mini">Storage • Analytics • Forecasting</div>
            <div class="metric-row">
                <div class="metric">
                    <div class="metric-label">Storage</div>
                    <div class="metric-value">ON</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Analytics</div>
                    <div class="metric-value">ON</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Forecasting</div>
                    <div class="metric-value">ON</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Output</div>
                    <div class="metric-value">HTTPS</div>
                </div>
            </div>
        </div>

        <div class="arrow">➜</div>

        <div id="stdLayer" class="layer std">
            <div class="layer-title">Standardization</div>
            <div class="mini">IEEE 2030.5 conversion</div>
            <div class="metric-row">
                <div class="metric">
                    <div class="metric-label">Format</div>
                    <div class="metric-value">2030.5</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Interoperability</div>
                    <div class="metric-value">YES</div>
                </div>
                <div class="metric">
                    <div class="metric-label">TLS</div>
                    <div class="metric-value">Later stage</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Ready for</div>
                    <div class="metric-value">ESBN</div>
                </div>
            </div>
        </div>
    </div>

    <div class="moving-area">
        <div class="track"></div>
        <div id="chip1" class="packet-chip chip1">Raw telemetry</div>
        <div id="chip2" class="packet-chip chip2">MQTT-ready packet</div>
        <div id="chip3" class="packet-chip chip3">Normalized JSON</div>
        <div id="chip4" class="packet-chip chip4">IEEE 2030.5 payload</div>
        <div id="chip5" class="packet-chip chip5">Control path</div>
    </div>

    <div class="packet-zone">
        <div id="leftZone"></div>
        <div id="rightZone"></div>
    </div>

    <div class="tiny-note">Minimal text, object-level view: raw device data → edge packet → normalized middleware object → IEEE 2030.5 utility payload.</div>
</div>

<script>
    const stageIndicator = document.getElementById("stageIndicator");
    const leftZone = document.getElementById("leftZone");
    const rightZone = document.getElementById("rightZone");

    const layers = {
        devices: document.getElementById("devicesLayer"),
        edge: document.getElementById("edgeLayer"),
        middleware: document.getElementById("middlewareLayer"),
        cloud: document.getElementById("cloudLayer"),
        std: document.getElementById("stdLayer"),
    };

    const chips = {
        chip1: document.getElementById("chip1"),
        chip2: document.getElementById("chip2"),
        chip3: document.getElementById("chip3"),
        chip4: document.getElementById("chip4"),
        chip5: document.getElementById("chip5"),
    };

    const rawPackets = `
<div class="packet raw visible">PV_01
protocol=Modbus
power_w=3000
voltage_v=230.4
frequency_hz=49.85</div>

<div class="packet raw visible">EV_01
protocol=OCPP
power_w=3600
charging_status=charging</div>

<div class="packet raw visible">HP_01
protocol=Modbus
power_w=1800
flow_temp_c=42.3</div>`;

    const edgePacket = `
<div class="packet edgepkt visible">EDGE_01
timestamp=2026-03-20T12:00:00
device_count=3
validation=OK
control_action=None
forward_protocol=MQTT-ready</div>`;

    const midPacket = `
<div class="packet midpkt visible">{
  "pv_generation_w": 3000,
  "total_demand_w": 5400,
  "net_balance_w": -2400,
  "operating_state": "Grid import required"
}</div>`;

    const cloudPacket = `
<div class="packet cloudpkt visible">cloud_status=received
analytics=enabled
forecasting=enabled
storage=active</div>`;

    const stdPacket = `
<div class="packet stdpkt visible">IEEE_2030.5_PAYLOAD
{
  "community_id": "SEC_01",
  "generation": 3000,
  "demand": 5400,
  "grid_status": "import_required"
}</div>`;

    const ctrlPacket = `
<div class="packet ctrlpkt visible">control_path
local_action=None
reason=monitoring_only</div>`;

    function resetVisuals() {
        Object.values(layers).forEach(el => el.classList.remove("active"));
        Object.values(chips).forEach(el => {
            el.className = el.className.split(" ").slice(0,2).join(" ");
            el.style.opacity = 0;
        });
        leftZone.innerHTML = "";
        rightZone.innerHTML = "";
    }

    function setStage(stage) {
        resetVisuals();

        if (stage === 0) {
            stageIndicator.innerText = "Stage 0 — Raw telemetry generation";
            layers.devices.classList.add("active");
            leftZone.innerHTML = rawPackets;
        }

        if (stage === 1) {
            stageIndicator.innerText = "Stage 1 — Raw packets collected by edge";
            layers.devices.classList.add("active");
            layers.edge.classList.add("active");
            leftZone.innerHTML = rawPackets;
            rightZone.innerHTML = edgePacket;
            chips.chip1.classList.add("animate1");
            chips.chip1.style.opacity = 1;
        }

        if (stage === 2) {
            stageIndicator.innerText = "Stage 2 — Edge creates unified MQTT-ready packet";
            layers.edge.classList.add("active");
            leftZone.innerHTML = edgePacket;
            chips.chip2.classList.add("animate2");
            chips.chip2.style.opacity = 1;
        }

        if (stage === 3) {
            stageIndicator.innerText = "Stage 3 — Middleware normalizes and aggregates";
            layers.middleware.classList.add("active");
            leftZone.innerHTML = edgePacket;
            rightZone.innerHTML = midPacket;
            chips.chip3.classList.add("animate3");
            chips.chip3.style.opacity = 1;
        }

        if (stage === 4) {
            stageIndicator.innerText = "Stage 4 — Cloud receives processed data";
            layers.cloud.classList.add("active");
            leftZone.innerHTML = midPacket;
            rightZone.innerHTML = cloudPacket;
            chips.chip4.classList.add("animate4");
            chips.chip4.style.opacity = 1;
        }

        if (stage === 5) {
            stageIndicator.innerText = "Stage 5 — IEEE 2030.5 payload sent to ESBN-facing stage";
            layers.std.classList.add("active");
            leftZone.innerHTML = cloudPacket + stdPacket;
            rightZone.innerHTML = ctrlPacket;
            chips.chip4.classList.add("animate4");
            chips.chip4.style.opacity = 1;
            chips.chip5.classList.add("animate5");
            chips.chip5.style.opacity = 1;
        }
    }

    async function playSimulation() {
        for (let s = 0; s <= 5; s++) {
            setStage(s);
            await new Promise(r => setTimeout(r, 1400));
        }
    }

    setStage(0);
</script>
</body>
</html>
"""

st.markdown("")
components.html(html_code, height=1400, scrolling=True)
