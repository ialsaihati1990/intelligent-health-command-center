
import streamlit as st
import pandas as pd
import numpy as np
import time
from pathlib import Path

st.set_page_config(
    page_title="Intelligent Health Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------------
# NHCC BRAND COLORS
# Source: National Health Command Center Brand Guidelines
# ------------------------------------------------------------------
NAVY = "#1B365D"
CYAN = "#00A3E0"
TEAL = "#007681"
APPLE = "#64A70B"
LIME = "#A9C23F"
GRAY = "#53565A"
RED = "#E4002B"
YELLOW = "#FFCD00"
WHITE = "#FFFFFF"
BG = "#F6F8FA"

ASSET_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSET_DIR / "moh_nhcc_logo.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    .block-container {{
        padding-top: 1.1rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}
    .hero {{
        background: linear-gradient(120deg, {NAVY} 0%, #102A49 62%, {TEAL} 100%);
        border-radius: 24px;
        padding: 30px 34px;
        color: white;
        box-shadow: 0 10px 30px rgba(27,54,93,.14);
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }}
    .hero:after {{
        content: "";
        position: absolute;
        right: -70px;
        bottom: -90px;
        width: 280px;
        height: 280px;
        border-radius: 50%;
        border: 40px solid rgba(0,163,224,.10);
    }}
    .hero-kicker {{
        font-size: 14px;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: #B8E4F5;
        font-weight: 700;
    }}
    .hero h1 {{
        margin: 7px 0 4px 0;
        font-size: 46px;
        line-height: 1.05;
        color: white;
        font-weight: 800;
    }}
    .hero h3 {{
        margin: 0;
        font-size: 22px;
        color: #D5E8F1;
        font-weight: 500;
    }}
    .demo-note {{
        background: #FFF8D9;
        border-left: 5px solid {YELLOW};
        padding: 12px 16px;
        border-radius: 12px;
        color: #4D4D4D;
        margin: 12px 0 20px 0;
        font-size: 15px;
    }}
    .section-title {{
        color: {NAVY};
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 8px;
    }}
    .scenario-card {{
        background: white;
        border: 1px solid #DFE7EC;
        border-radius: 18px;
        padding: 18px;
        min-height: 190px;
        box-shadow: 0 4px 14px rgba(27,54,93,.06);
    }}
    .scenario-card h4 {{
        color: {NAVY};
        margin: 4px 0 6px 0;
        font-size: 19px;
    }}
    .scenario-card p {{
        color: {GRAY};
        font-size: 14px;
        line-height: 1.45;
    }}
    .chip {{
        display: inline-block;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        background: #EAF7FB;
        color: {TEAL};
        margin-right: 5px;
        margin-top: 5px;
    }}
    .agent {{
        background: white;
        border: 1px solid #E0E7EB;
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        min-height: 126px;
        box-shadow: 0 4px 14px rgba(27,54,93,.05);
    }}
    .agent .icon {{
        font-size: 30px;
    }}
    .agent .name {{
        color: {NAVY};
        font-weight: 800;
        font-size: 15px;
    }}
    .agent .status {{
        color: {TEAL};
        font-size: 12px;
        margin-top: 5px;
    }}
    .supervisor {{
        background: linear-gradient(120deg, {TEAL}, {NAVY});
        color: white;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(0,118,129,.16);
    }}
    .priority-high {{
        background: #FDECEC;
        color: #A61B1B;
        border: 1px solid #F2BABA;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 800;
        display: inline-block;
    }}
    .priority-medium {{
        background: #FFF6D6;
        color: #866000;
        border: 1px solid #F2D779;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 800;
        display: inline-block;
    }}
    .exec-card {{
        background: white;
        border-radius: 22px;
        padding: 23px;
        box-shadow: 0 8px 26px rgba(27,54,93,.08);
        border-top: 6px solid {TEAL};
        margin-top: 12px;
    }}
    .exec-label {{
        color: {TEAL};
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .08em;
    }}
    .exec-text {{
        color: {NAVY};
        font-size: 17px;
        line-height: 1.5;
        margin-top: 4px;
    }}
    .human {{
        background: {NAVY};
        color: white;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        margin-top: 16px;
    }}
    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid #E1E7EB;
        padding: 12px 14px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(27,54,93,.04);
    }}
    .small-muted {{
        color: {GRAY};
        font-size: 13px;
    }}
    .footer {{
        text-align: center;
        color: #6E7A84;
        font-size: 12px;
        padding-top: 28px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# SYNTHETIC DATA
# ------------------------------------------------------------------
@st.cache_data
def generate_demo_data(seed=26):
    rng = np.random.default_rng(seed)
    facilities = [f"Facility {i:02d}" for i in range(1, 13)]
    zones = ["Central", "North", "East", "West"]
    rows = []

    for i, f in enumerate(facilities):
        zone = zones[i % len(zones)]
        ed_wait = np.clip(rng.normal(105, 28), 45, 220)
        occupancy = np.clip(rng.normal(84, 8), 55, 99)
        los = np.clip(rng.normal(4.7, 1.15), 2.2, 9.0)
        lab_tat = np.clip(rng.normal(72, 19), 30, 160)
        discharge_delay = np.clip(rng.normal(16, 6), 3, 35)
        critical_labs = int(np.clip(rng.normal(6, 3), 0, 16))

        rows.append({
            "Facility": f,
            "Zone": zone,
            "ED Wait (min)": round(ed_wait),
            "Bed Occupancy (%)": round(occupancy, 1),
            "LOS (days)": round(los, 1),
            "Lab TAT (min)": round(lab_tat),
            "Discharge Delays": round(discharge_delay),
            "Critical Lab Alerts": critical_labs
        })

    df = pd.DataFrame(rows)

    # Build an intentional exhibition pattern so the agentic story is clear.
    df.loc[df["Facility"] == "Facility 07", ["ED Wait (min)", "Bed Occupancy (%)", "LOS (days)", "Discharge Delays"]] = [188, 97.2, 7.8, 31]
    df.loc[df["Facility"] == "Facility 03", ["ED Wait (min)", "Bed Occupancy (%)", "LOS (days)"]] = [164, 94.5, 6.9]
    df.loc[df["Facility"] == "Facility 10", ["Lab TAT (min)", "Critical Lab Alerts"]] = [143, 13]

    return df

df = generate_demo_data()

SCENARIOS = {
    "Emergency Department Pressure": {
        "icon": "🚑",
        "tagline": "Detect ED pressure and connect it to downstream capacity constraints.",
        "agents": ["ED Agent", "Bed Agent", "LOS Agent"],
        "question": "Which facilities show the highest ED operational pressure today?",
        "metric": "ED Wait (min)"
    },
    "Bed Capacity & Patient Flow": {
        "icon": "🛏️",
        "tagline": "Identify capacity bottlenecks and patient-flow constraints.",
        "agents": ["Bed Agent", "LOS Agent", "Discharge Agent"],
        "question": "Where are bed capacity and patient flow most constrained?",
        "metric": "Bed Occupancy (%)"
    },
    "Laboratory Performance": {
        "icon": "🧪",
        "tagline": "Surface delayed turnaround times and critical laboratory signals.",
        "agents": ["Lab Agent", "Quality Agent", "Operations Agent"],
        "question": "Which facilities need attention for laboratory performance?",
        "metric": "Lab TAT (min)"
    },
    "Cross-Service Operational Risk": {
        "icon": "🧠",
        "tagline": "Connect multiple operational signals to create one prioritized view.",
        "agents": ["ED Agent", "Bed Agent", "LOS Agent", "Lab Agent"],
        "question": "Which facility needs attention first, and what is driving the risk?",
        "metric": "Composite"
    }
}

def calc_risk(data):
    z = data.copy()
    z["Risk Score"] = (
        0.30 * np.clip((z["ED Wait (min)"] - 90) / 100, 0, 1) +
        0.25 * np.clip((z["Bed Occupancy (%)"] - 80) / 20, 0, 1) +
        0.20 * np.clip((z["LOS (days)"] - 4) / 5, 0, 1) +
        0.15 * np.clip((z["Lab TAT (min)"] - 60) / 100, 0, 1) +
        0.10 * np.clip((z["Discharge Delays"] - 10) / 25, 0, 1)
    ) * 100
    return z.sort_values("Risk Score", ascending=False)

risk_df = calc_risk(df)

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
top1, top2 = st.columns([1, 4])
with top1:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
with top2:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">National Health Command Center</div>
            <h1>Intelligent Health Command Center</h1>
            <h3>Powered by Agentic AI · From Real-Time Signals to Intelligent Decision Support</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="demo-note">
    <b>Demonstration environment:</b> All names, facilities, values, alerts, and results shown in this prototype are
    <b>synthetically generated and do not represent real Ministry of Health data.</b>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# EXPERIENCE STEP 1 — CHOOSE SCENARIO
# ------------------------------------------------------------------
st.markdown('<div class="section-title">1 · Choose a Scenario</div>', unsafe_allow_html=True)

cols = st.columns(4)
for col, (name, meta) in zip(cols, SCENARIOS.items()):
    with col:
        st.markdown(
            f"""
            <div class="scenario-card">
                <div style="font-size:34px">{meta['icon']}</div>
                <h4>{name}</h4>
                <p>{meta['tagline']}</p>
                <span class="chip">{len(meta['agents'])} AI Agents</span>
                <span class="chip">Human Oversight</span>
            </div>
            """,
            unsafe_allow_html=True
        )

scenario = st.selectbox(
    "Select the scenario to run",
    list(SCENARIOS.keys()),
    index=3,
    label_visibility="collapsed"
)

st.markdown('<div class="section-title">2 · Ask the Command Center</div>', unsafe_allow_html=True)
default_q = SCENARIOS[scenario]["question"]
question = st.text_input(
    "Question",
    value=default_q,
    placeholder="Ask an operational question...",
    label_visibility="collapsed"
)

run = st.button("Run Agentic Analysis", type="primary", use_container_width=True)

# ------------------------------------------------------------------
# EXPERIENCE STEP 2 — AGENTS AT WORK
# ------------------------------------------------------------------
if run:
    st.session_state["last_scenario"] = scenario
    st.session_state["question"] = question

if "last_scenario" in st.session_state:
    active = st.session_state["last_scenario"]
    meta = SCENARIOS[active]

    st.markdown('<div class="section-title">3 · Agents at Work</div>', unsafe_allow_html=True)

    progress = st.progress(0, text="Initializing specialized agents...")
    for p, msg in [
        (18, "Reading synthetic operational signals..."),
        (38, "Specialized agents analyzing their domains..."),
        (60, "Connecting signals across services..."),
        (82, "Supervisor Agent prioritizing operational impact..."),
        (100, "Executive insight ready.")
    ]:
        time.sleep(0.28)
        progress.progress(p, text=msg)

    agent_cols = st.columns(len(meta["agents"]))
    icons = ["🚑", "🛏️", "⏱️", "🧪", "📊", "🔎"]
    for i, (col, agent) in enumerate(zip(agent_cols, meta["agents"])):
        with col:
            st.markdown(
                f"""
                <div class="agent">
                    <div class="icon">{icons[i]}</div>
                    <div class="name">{agent}</div>
                    <div class="status">Analysis complete ✓</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div style="text-align:center;font-size:28px;color:#007681;margin:8px 0">↓</div>
        <div class="supervisor">
            🧠 Supervisor Agent · Connecting findings · Assessing impact · Prioritizing attention
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------------
    # LIVE / SYNTHETIC DATA VIEW
    # ------------------------------------------------------------------
    st.markdown('<div class="section-title">4 · Operational Signals</div>', unsafe_allow_html=True)

    if active == "Emergency Department Pressure":
        view = df.sort_values("ED Wait (min)", ascending=False).head(5)
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest ED Wait", f"{view.iloc[0]['ED Wait (min)']} min")
        c2.metric("Associated Bed Occupancy", f"{view.iloc[0]['Bed Occupancy (%)']:.1f}%")
        c3.metric("Associated LOS", f"{view.iloc[0]['LOS (days)']:.1f} days")
        st.bar_chart(view.set_index("Facility")[["ED Wait (min)"]])

    elif active == "Bed Capacity & Patient Flow":
        view = df.sort_values(["Bed Occupancy (%)", "LOS (days)"], ascending=False).head(5)
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest Occupancy", f"{view.iloc[0]['Bed Occupancy (%)']:.1f}%")
        c2.metric("LOS", f"{view.iloc[0]['LOS (days)']:.1f} days")
        c3.metric("Discharge Delays", f"{int(view.iloc[0]['Discharge Delays'])}")
        st.bar_chart(view.set_index("Facility")[["Bed Occupancy (%)"]])

    elif active == "Laboratory Performance":
        view = df.sort_values("Lab TAT (min)", ascending=False).head(5)
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest Lab TAT", f"{view.iloc[0]['Lab TAT (min)']} min")
        c2.metric("Critical Alerts", f"{int(view.iloc[0]['Critical Lab Alerts'])}")
        c3.metric("Facility", view.iloc[0]["Facility"])
        st.bar_chart(view.set_index("Facility")[["Lab TAT (min)"]])

    else:
        view = risk_df.head(5)
        top = view.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Highest Risk Score", f"{top['Risk Score']:.0f}/100")
        c2.metric("ED Wait", f"{int(top['ED Wait (min)'])} min")
        c3.metric("Bed Occupancy", f"{top['Bed Occupancy (%)']:.1f}%")
        c4.metric("LOS", f"{top['LOS (days)']:.1f} days")
        st.bar_chart(view.set_index("Facility")[["Risk Score"]])

    with st.expander("View synthetic demonstration data"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------------
    # EXECUTIVE INTELLIGENCE CARD
    # ------------------------------------------------------------------
    top = risk_df.iloc[0]
    facility = top["Facility"]

    if active == "Laboratory Performance":
        lab_top = df.sort_values("Lab TAT (min)", ascending=False).iloc[0]
        facility = lab_top["Facility"]
        priority = "HIGH" if lab_top["Lab TAT (min)"] >= 120 else "MEDIUM"
        situation = f"{facility} shows the highest laboratory turnaround time in the demonstration dataset."
        why = "Delayed turnaround combined with critical alerts may affect operational responsiveness and requires review."
        drivers = f"Lab TAT {int(lab_top['Lab TAT (min)'])} min · Critical alerts {int(lab_top['Critical Lab Alerts'])}"
        action = "Review laboratory workflow, critical-result escalation, and staffing/capacity conditions before any operational action is taken."
    elif active == "Emergency Department Pressure":
        ed_top = df.sort_values("ED Wait (min)", ascending=False).iloc[0]
        facility = ed_top["Facility"]
        priority = "HIGH"
        situation = f"{facility} shows the highest ED pressure signal in the demonstration dataset."
        why = "ED waiting is occurring alongside high bed occupancy and extended length of stay, indicating a potential downstream flow constraint."
        drivers = f"ED wait {int(ed_top['ED Wait (min)'])} min · Occupancy {ed_top['Bed Occupancy (%)']:.1f}% · LOS {ed_top['LOS (days)']:.1f} days"
        action = "Review patient flow, available capacity, and discharge constraints with the responsible operational teams."
    elif active == "Bed Capacity & Patient Flow":
        bed_top = df.sort_values(["Bed Occupancy (%)", "LOS (days)"], ascending=False).iloc[0]
        facility = bed_top["Facility"]
        priority = "HIGH" if bed_top["Bed Occupancy (%)"] >= 95 else "MEDIUM"
        situation = f"{facility} shows the strongest bed-capacity and patient-flow constraint."
        why = "High occupancy is combined with prolonged LOS and discharge delays, creating a potential bottleneck in patient movement."
        drivers = f"Occupancy {bed_top['Bed Occupancy (%)']:.1f}% · LOS {bed_top['LOS (days)']:.1f} days · Delayed discharges {int(bed_top['Discharge Delays'])}"
        action = "Review discharge readiness, bed turnover, and upstream/downstream flow constraints with operational teams."
    else:
        priority = "HIGH"
        situation = f"{facility} is the highest-priority facility after connecting ED, bed, LOS, laboratory, and discharge signals."
        why = "No single indicator explains the situation. The priority emerges from multiple connected operational signals occurring together."
        drivers = (
            f"ED wait {int(top['ED Wait (min)'])} min · "
            f"Occupancy {top['Bed Occupancy (%)']:.1f}% · "
            f"LOS {top['LOS (days)']:.1f} days · "
            f"Lab TAT {int(top['Lab TAT (min)'])} min · "
            f"Delayed discharges {int(top['Discharge Delays'])}"
        )
        action = "Initiate an operational review of patient flow and capacity drivers, validate the evidence with responsible teams, then determine the appropriate intervention."

    st.markdown('<div class="section-title">5 · Executive Intelligence</div>', unsafe_allow_html=True)
    badge = "priority-high" if priority == "HIGH" else "priority-medium"

    st.markdown(
        f"""
        <div class="exec-card">
            <div class="{badge}">{priority} PRIORITY</div>
            <h2 style="color:{NAVY};margin:12px 0 4px 0">{facility}</h2>

            <div class="exec-label">What is happening?</div>
            <div class="exec-text">{situation}</div><br>

            <div class="exec-label">Why does it matter?</div>
            <div class="exec-text">{why}</div><br>

            <div class="exec-label">Key connected drivers</div>
            <div class="exec-text">{drivers}</div><br>

            <div class="exec-label">Recommended attention</div>
            <div class="exec-text">{action}</div>
        </div>

        <div class="human">
            AI Recommends. Humans Decide. &nbsp; · &nbsp; Human-in-the-Loop
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title">6 · Human Decision</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        if st.button("Review Evidence", use_container_width=True):
            st.info("Evidence view opened. In the exhibition prototype, this would show the indicators and source trail used by the agents.")
    with d2:
        if st.button("Explore Another Scenario", use_container_width=True):
            st.info("Select another scenario above to demonstrate cross-domain Agentic AI behavior.")
    with d3:
        if st.button("Acknowledge for Review", type="primary", use_container_width=True):
            st.success("Acknowledged for human operational review. No automated operational action has been executed.")

st.markdown(
    """
    <div class="footer">
    Prototype for visitor-experience testing · Synthetic demonstration data only · No real patient, facility, or Ministry of Health operational data is used.
    </div>
    """,
    unsafe_allow_html=True
)
