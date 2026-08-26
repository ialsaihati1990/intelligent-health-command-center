
import streamlit as st
import pandas as pd
import numpy as np
import time
import textwrap
from pathlib import Path

st.set_page_config(
    page_title="Intelligent Health Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# NHCC BRAND COLORS
# =========================
NAVY = "#1B365D"
CYAN = "#00A3E0"
TEAL = "#007681"
APPLE = "#64A70B"
LIME = "#A9C23F"
GRAY = "#53565A"
RED = "#E4002B"
YELLOW = "#FFCD00"
WHITE = "#FFFFFF"
BG = "#F4F7F9"

ASSET_DIR = Path("assets")
LOGO_PATH = ASSET_DIR / "moh_nhcc_logo.png"

def render_html(html):
    """Render HTML safely without Markdown interpreting indentation as code."""
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


# =========================
# GLOBAL CSS
# =========================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: Inter, Arial, sans-serif;
}}
.stApp {{
    background:
      radial-gradient(circle at top right, rgba(0,163,224,.07), transparent 22%),
      linear-gradient(180deg, #F8FBFC 0%, {BG} 100%);
}}
[data-testid="stHeader"] {{ background: rgba(255,255,255,0); }}
.block-container {{
    padding-top: 0.4rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}}

.hero {{
    background:
      radial-gradient(circle at 89% 45%, rgba(0,163,224,.22) 0%, rgba(0,163,224,0) 20%),
      linear-gradient(118deg, #102B4A 0%, {NAVY} 52%, {TEAL} 100%);
    border-radius: 28px;
    padding: 28px 30px;
    color: white;
    box-shadow: 0 16px 40px rgba(27,54,93,.18);
    border: 1px solid rgba(255,255,255,.08);
    margin-bottom: 18px;
}}
.hero-grid {{
    display:grid;
    grid-template-columns: 270px 1fr 290px;
    gap: 26px;
    align-items:center;
}}
.logo-panel {{
    background: rgba(255,255,255,.96);
    border-radius: 22px;
    padding: 18px;
    display:flex;
    align-items:center;
    justify-content:center;
    min-height:150px;
}}
.hero-kicker {{
    color:#BDEBFA;
    letter-spacing:.16em;
    font-size:13px;
    font-weight:800;
}}
.hero-title {{
    font-size:48px;
    line-height:1.03;
    font-weight:850;
    margin:8px 0 8px 0;
}}
.hero-sub {{
    color:#D9EEF5;
    font-size:21px;
    font-weight:500;
}}
.demo-chip {{
    border:1px solid rgba(255,255,255,.25);
    background:rgba(4,45,67,.45);
    border-radius:18px;
    padding:16px;
    color:#EAF7FB;
    font-size:13px;
    line-height:1.5;
}}

.nav-strip {{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:10px;
    margin:18px 0 28px 0;
}}
.nav-step {{
    background:white;
    border:1px solid #DFE8ED;
    border-radius:16px;
    padding:13px 14px;
    box-shadow:0 4px 12px rgba(27,54,93,.04);
    color:{NAVY};
    font-weight:800;
    font-size:13px;
}}
.nav-step span {{
    color:{TEAL};
    margin-right:5px;
}}

.section-title {{
    color:{NAVY};
    font-size:28px;
    font-weight:850;
    margin:18px 0 12px 0;
}}
.section-sub {{
    color:#6A7782;
    font-size:14px;
    margin-top:-6px;
    margin-bottom:15px;
}}

.scenario-card {{
    background:white;
    border:1px solid #DEE7EC;
    border-radius:22px;
    padding:20px;
    min-height:225px;
    box-shadow:0 10px 24px rgba(27,54,93,.06);
    transition:transform .2s ease, box-shadow .2s ease;
}}
.scenario-card:hover {{
    transform:translateY(-4px);
    box-shadow:0 18px 34px rgba(27,54,93,.10);
}}
.scenario-icon {{
    font-size:38px;
}}
.scenario-title {{
    color:{NAVY};
    font-size:19px;
    font-weight:850;
    margin:8px 0 7px 0;
}}
.scenario-copy {{
    color:#65727D;
    font-size:14px;
    line-height:1.5;
}}
.badge {{
    display:inline-block;
    padding:5px 9px;
    background:#ECF8FB;
    color:{TEAL};
    border-radius:999px;
    font-size:11px;
    font-weight:800;
    margin:4px 3px 0 0;
}}

.ask-card {{
    background:linear-gradient(120deg,#FFFFFF,#F2FBFD);
    border:1px solid #DDE9EE;
    border-radius:22px;
    padding:18px 20px;
    box-shadow:0 8px 20px rgba(27,54,93,.05);
}}

.agent-card {{
    background:white;
    border:1px solid #DFE8ED;
    border-radius:20px;
    padding:18px 12px;
    text-align:center;
    min-height:150px;
    box-shadow:0 8px 18px rgba(27,54,93,.05);
}}
.agent-icon {{ font-size:32px; }}
.agent-name {{ color:{NAVY}; font-weight:850; font-size:15px; margin-top:6px; }}
.agent-state {{ color:{TEAL}; font-size:12px; margin-top:5px; }}
.supervisor {{
    background:linear-gradient(120deg,{TEAL},{NAVY});
    color:white;
    border-radius:20px;
    padding:18px;
    text-align:center;
    font-size:17px;
    font-weight:800;
    box-shadow:0 12px 28px rgba(0,118,129,.16);
}}
.metric-shell {{
    background:white;
    border:1px solid #DEE7EC;
    border-radius:20px;
    padding:18px;
    box-shadow:0 8px 18px rgba(27,54,93,.05);
}}

.exec-card {{
    background:white;
    border-radius:24px;
    padding:25px;
    box-shadow:0 14px 35px rgba(27,54,93,.09);
    border-top:6px solid {TEAL};
}}
.priority {{
    display:inline-block;
    padding:6px 11px;
    border-radius:999px;
    background:#FDEBEB;
    color:#B42318;
    border:1px solid #F8B4B4;
    font-size:12px;
    font-weight:900;
}}
.exec-block {{
    display:grid;
    grid-template-columns:52px 1fr;
    gap:12px;
    padding:15px 0;
    border-bottom:1px dashed #DDE5EA;
}}
.exec-icon {{
    width:42px;height:42px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    border:1px solid #9FD5DD;
    color:{TEAL};
    font-size:20px;
}}
.exec-label {{
    color:{TEAL};
    font-size:13px;
    font-weight:900;
}}
.exec-text {{
    color:{NAVY};
    font-size:16px;
    line-height:1.45;
    margin-top:3px;
}}
.driver-pill {{
    display:inline-block;
    background:#EEF3F7;
    color:{NAVY};
    border-radius:10px;
    padding:7px 10px;
    margin:3px 4px 0 0;
    font-size:13px;
    font-weight:700;
}}

.human-card {{
    margin-top:16px;
    background:{NAVY};
    color:white;
    border-radius:18px;
    padding:18px;
    text-align:center;
    font-size:18px;
    font-weight:900;
}}

[data-testid="stMetric"] {{
    background:white;
    border:1px solid #DFE7EC;
    padding:14px;
    border-radius:16px;
    box-shadow:0 5px 13px rgba(27,54,93,.04);
}}

div.stButton > button {{
    border-radius:14px;
    min-height:46px;
    font-weight:800;
}}

.footer {{
    text-align:center;
    color:#7A8791;
    font-size:12px;
    padding:28px 0 8px 0;
}}

@media (max-width: 900px) {{
    .hero-grid {{ grid-template-columns:1fr; }}
    .nav-strip {{ grid-template-columns:1fr 1fr; }}
    .hero-title {{ font-size:36px; }}
}}

/* Booth mode polish */
[data-testid="stToolbar"] {
    opacity: .35;
    transition: opacity .2s ease;
}
[data-testid="stToolbar"]:hover {
    opacity: 1;
}
a.header-anchor, .stMarkdown a[href^="#"] {
    text-decoration: none !important;
}
.exec-card pre, .exec-card code {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SYNTHETIC DATA
# =========================
@st.cache_data
def generate_demo_data(seed=26):
    rng = np.random.default_rng(seed)
    facilities = [f"Facility {i:02d}" for i in range(1, 13)]
    zones = ["Central", "North", "East", "West"]
    rows = []
    for i, f in enumerate(facilities):
        rows.append({
            "Facility": f,
            "Zone": zones[i % 4],
            "ED Wait (min)": int(np.clip(rng.normal(105, 28), 45, 220)),
            "Bed Occupancy (%)": round(float(np.clip(rng.normal(84, 8), 55, 99)), 1),
            "LOS (days)": round(float(np.clip(rng.normal(4.7, 1.15), 2.2, 9.0)), 1),
            "Lab TAT (min)": int(np.clip(rng.normal(72, 19), 30, 160)),
            "Discharge Delays": int(np.clip(rng.normal(16, 6), 3, 35)),
            "Critical Lab Alerts": int(np.clip(rng.normal(6, 3), 0, 16))
        })

    df = pd.DataFrame(rows)
    df.loc[df["Facility"] == "Facility 07", ["ED Wait (min)","Bed Occupancy (%)","LOS (days)","Discharge Delays"]] = [188,97.2,7.8,31]
    df.loc[df["Facility"] == "Facility 03", ["ED Wait (min)","Bed Occupancy (%)","LOS (days)"]] = [164,94.5,6.9]
    df.loc[df["Facility"] == "Facility 10", ["Lab TAT (min)","Critical Lab Alerts"]] = [143,13]
    return df

df = generate_demo_data()

def calc_risk(data):
    z = data.copy()
    z["Risk Score"] = (
        .30*np.clip((z["ED Wait (min)"]-90)/100,0,1) +
        .25*np.clip((z["Bed Occupancy (%)"]-80)/20,0,1) +
        .20*np.clip((z["LOS (days)"]-4)/5,0,1) +
        .15*np.clip((z["Lab TAT (min)"]-60)/100,0,1) +
        .10*np.clip((z["Discharge Delays"]-10)/25,0,1)
    )*100
    return z.sort_values("Risk Score", ascending=False)

risk_df = calc_risk(df)

SCENARIOS = {
    "Emergency Department Pressure": {
        "icon":"🚑",
        "tagline":"Detect ED pressure and connect it to downstream capacity constraints.",
        "agents":["ED Agent","Bed Agent","LOS Agent"],
        "question":"Which facilities show the highest ED operational pressure today?"
    },
    "Bed Capacity & Patient Flow": {
        "icon":"🛏️",
        "tagline":"Identify capacity bottlenecks and patient-flow constraints.",
        "agents":["Bed Agent","LOS Agent","Discharge Agent"],
        "question":"Where are bed capacity and patient flow most constrained?"
    },
    "Laboratory Performance": {
        "icon":"🧪",
        "tagline":"Surface delayed turnaround times and critical laboratory signals.",
        "agents":["Lab Agent","Quality Agent","Operations Agent"],
        "question":"Which facilities need attention for laboratory performance?"
    },
    "Cross-Service Operational Risk": {
        "icon":"🧠",
        "tagline":"Connect multiple operational signals into one prioritized view.",
        "agents":["ED Agent","Bed Agent","LOS Agent","Lab Agent"],
        "question":"Which facility needs attention first, and what is driving the risk?"
    }
}

# =========================
# HEADER
# =========================
logo_html = ""
if LOGO_PATH.exists():
    import base64
    data = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    logo_html = f'<img src="data:image/jpeg;base64,{data}" style="max-width:100%;height:auto;border-radius:12px;">'
else:
    logo_html = '<div style="color:#1B365D;font-weight:900;font-size:22px">MOH + NHCC</div>'

st.markdown(f"""
<div class="hero">
  <div class="hero-grid">
    <div class="logo-panel">{logo_html}</div>
    <div>
      <div class="hero-kicker">National Health Command Center</div>
      <div class="hero-title">Intelligent Health Command Center</div>
      <div class="hero-sub">Powered by Agentic AI · From Real-Time Signals to Intelligent Decision Support</div>
    </div>
    <div class="demo-chip">
      <b>DEMO DATA ONLY</b><br>
      All facility names, values, alerts, and recommendations are synthetically generated for demonstration purposes and do not represent real Ministry of Health data.
    </div>
  </div>
</div>

<div class="nav-strip">
  <div class="nav-step"><span>1</span> Select Scenario</div>
  <div class="nav-step"><span>2</span> Ask a Question</div>
  <div class="nav-step"><span>3</span> Agents at Work</div>
  <div class="nav-step"><span>4</span> Executive Intelligence</div>
  <div class="nav-step"><span>5</span> Human Decision</div>
</div>
""", unsafe_allow_html=True)

# =========================
# STEP 1
# =========================
st.markdown('<div class="section-title">1 · Choose a Scenario</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Pick a story the visitor can understand in seconds.</div>', unsafe_allow_html=True)

cols = st.columns(4)
for col, (name, meta) in zip(cols, SCENARIOS.items()):
    with col:
        st.markdown(f"""
        <div class="scenario-card">
          <div class="scenario-icon">{meta['icon']}</div>
          <div class="scenario-title">{name}</div>
          <div class="scenario-copy">{meta['tagline']}</div>
          <div>
            <span class="badge">{len(meta['agents'])} AI Agents</span>
            <span class="badge">Human Oversight</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

scenario = st.radio(
    "Scenario",
    list(SCENARIOS.keys()),
    index=3,
    horizontal=True,
    label_visibility="collapsed"
)

# =========================
# STEP 2
# =========================
st.markdown('<div class="section-title">2 · Ask the Command Center</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Natural-language interaction keeps the booth experience simple and memorable.</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="ask-card">', unsafe_allow_html=True)
    q = st.text_input(
        "Ask a question",
        value=SCENARIOS[scenario]["question"],
        label_visibility="collapsed"
    )
    cta1, cta2 = st.columns([4,1])
    with cta1:
        run = st.button("▶ Run Agentic Analysis", type="primary", use_container_width=True)
    with cta2:
        st.button("Reset", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if run:
    st.session_state["active_scenario"] = scenario

if "active_scenario" in st.session_state:
    active = st.session_state["active_scenario"]
    meta = SCENARIOS[active]

    # =========================
    # STEP 3
    # =========================
    st.markdown('<div class="section-title">3 · Agents at Work</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">The visitor sees specialized agents working before the Supervisor Agent connects the story.</div>', unsafe_allow_html=True)

    progress = st.progress(0, text="Initializing specialized agents...")
    steps = [
        (20, "Reading synthetic operational signals..."),
        (40, "Specialized agents analyzing their domains..."),
        (62, "Connecting signals across services..."),
        (82, "Supervisor Agent assessing operational impact..."),
        (100, "Executive insight ready.")
    ]
    for p, msg in steps:
        time.sleep(.22)
        progress.progress(p, text=msg)

    acols = st.columns(len(meta["agents"]))
    icons = ["🚑","🛏️","⏱️","🧪"]
    for i, (col, agent) in enumerate(zip(acols, meta["agents"])):
        with col:
            st.markdown(f"""
            <div class="agent-card">
              <div class="agent-icon">{icons[i]}</div>
              <div class="agent-name">{agent}</div>
              <div class="agent-state">Analysis complete ✓</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;font-size:28px;color:#007681;margin:7px 0">↓</div>', unsafe_allow_html=True)
    st.markdown('<div class="supervisor">🧠 Supervisor Agent · Connects findings · Assesses impact · Prioritizes attention</div>', unsafe_allow_html=True)

    # =========================
    # STEP 4: OPERATIONAL SIGNALS
    # =========================
    st.markdown('<div class="section-title">4 · Operational Signals</div>', unsafe_allow_html=True)

    if active == "Emergency Department Pressure":
        view = df.sort_values("ED Wait (min)", ascending=False).head(5)
        top = view.iloc[0]
        c1,c2,c3 = st.columns(3)
        c1.metric("Highest ED Wait", f"{int(top['ED Wait (min)'])} min")
        c2.metric("Bed Occupancy", f"{top['Bed Occupancy (%)']:.1f}%")
        c3.metric("LOS", f"{top['LOS (days)']:.1f} days")
        st.bar_chart(view.set_index("Facility")[["ED Wait (min)"]], use_container_width=True)

    elif active == "Bed Capacity & Patient Flow":
        view = df.sort_values(["Bed Occupancy (%)","LOS (days)"], ascending=False).head(5)
        top = view.iloc[0]
        c1,c2,c3 = st.columns(3)
        c1.metric("Highest Occupancy", f"{top['Bed Occupancy (%)']:.1f}%")
        c2.metric("LOS", f"{top['LOS (days)']:.1f} days")
        c3.metric("Discharge Delays", f"{int(top['Discharge Delays'])}")
        st.bar_chart(view.set_index("Facility")[["Bed Occupancy (%)"]], use_container_width=True)

    elif active == "Laboratory Performance":
        view = df.sort_values("Lab TAT (min)", ascending=False).head(5)
        top = view.iloc[0]
        c1,c2,c3 = st.columns(3)
        c1.metric("Highest Lab TAT", f"{int(top['Lab TAT (min)'])} min")
        c2.metric("Critical Alerts", f"{int(top['Critical Lab Alerts'])}")
        c3.metric("Facility", top["Facility"])
        st.bar_chart(view.set_index("Facility")[["Lab TAT (min)"]], use_container_width=True)

    else:
        view = risk_df.head(5)
        top = view.iloc[0]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Risk Score", f"{top['Risk Score']:.0f}/100")
        c2.metric("ED Wait", f"{int(top['ED Wait (min)'])} min")
        c3.metric("Bed Occupancy", f"{top['Bed Occupancy (%)']:.1f}%")
        c4.metric("LOS", f"{top['LOS (days)']:.1f} days")
        st.bar_chart(view.set_index("Facility")[["Risk Score"]], use_container_width=True)

    with st.expander("View synthetic demonstration data"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    # =========================
    # STEP 5: EXECUTIVE INTELLIGENCE
    # =========================
    st.markdown('<div class="section-title">5 · Executive Intelligence</div>', unsafe_allow_html=True)

    top = risk_df.iloc[0]
    if active == "Emergency Department Pressure":
        rec = df.sort_values("ED Wait (min)", ascending=False).iloc[0]
        facility = rec["Facility"]
        situation = f"{facility} shows the highest ED pressure signal in the demonstration dataset."
        why = "ED waiting is occurring alongside high bed occupancy and extended length of stay, indicating a potential downstream patient-flow constraint."
        drivers = [
            f"ED wait {int(rec['ED Wait (min)'])} min",
            f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",
            f"LOS {rec['LOS (days)']:.1f} days"
        ]
        action = "Review patient flow, available capacity, and discharge constraints with the responsible operational teams."

    elif active == "Bed Capacity & Patient Flow":
        rec = df.sort_values(["Bed Occupancy (%)","LOS (days)"], ascending=False).iloc[0]
        facility = rec["Facility"]
        situation = f"{facility} shows the strongest combined bed-capacity and patient-flow constraint."
        why = "High occupancy is occurring together with prolonged LOS and delayed discharges, suggesting a potential flow bottleneck."
        drivers = [
            f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",
            f"LOS {rec['LOS (days)']:.1f} days",
            f"Delayed discharges {int(rec['Discharge Delays'])}"
        ]
        action = "Review discharge readiness, bed turnover, and upstream/downstream flow constraints."

    elif active == "Laboratory Performance":
        rec = df.sort_values("Lab TAT (min)", ascending=False).iloc[0]
        facility = rec["Facility"]
        situation = f"{facility} shows the highest laboratory turnaround time in the demonstration dataset."
        why = "Delayed turnaround combined with critical alerts may affect operational responsiveness and requires further validation."
        drivers = [
            f"Lab TAT {int(rec['Lab TAT (min)'])} min",
            f"Critical alerts {int(rec['Critical Lab Alerts'])}"
        ]
        action = "Review laboratory workflow, critical-result escalation, and capacity conditions with the responsible teams."

    else:
        rec = risk_df.iloc[0]
        facility = rec["Facility"]
        situation = f"{facility} is the highest-priority facility after connecting ED, bed, LOS, laboratory, and discharge signals."
        why = "The priority does not come from one indicator alone. It emerges from several operational signals occurring together."
        drivers = [
            f"ED wait {int(rec['ED Wait (min)'])} min",
            f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",
            f"LOS {rec['LOS (days)']:.1f} days",
            f"Lab TAT {int(rec['Lab TAT (min)'])} min",
            f"Delayed discharges {int(rec['Discharge Delays'])}"
        ]
        action = "Initiate a focused operational review, validate the evidence with responsible teams, and then determine the appropriate intervention."

    pills = "".join([f'<span class="driver-pill">{d}</span>' for d in drivers])

    exec_html = f"""
<div class="exec-card">
  <span class="priority">HIGH PRIORITY</span>
  <h2 style="color:{NAVY};font-size:34px;margin:14px 0 6px 0;">{facility}</h2>

  <div class="exec-block">
    <div class="exec-icon">⌁</div>
    <div>
      <div class="exec-label">What is happening?</div>
      <div class="exec-text">{situation}</div>
    </div>
  </div>

  <div class="exec-block">
    <div class="exec-icon">?</div>
    <div>
      <div class="exec-label">Why does it matter?</div>
      <div class="exec-text">{why}</div>
    </div>
  </div>

  <div class="exec-block">
    <div class="exec-icon">▥</div>
    <div>
      <div class="exec-label">Key connected drivers</div>
      <div class="exec-text">{pills}</div>
    </div>
  </div>

  <div class="exec-block" style="border-bottom:none;">
    <div class="exec-icon">◎</div>
    <div>
      <div class="exec-label">Recommended attention</div>
      <div class="exec-text">{action}</div>
    </div>
  </div>
</div>

<div class="human-card">
  AI Recommends. Humans Decide. · Human-in-the-Loop
</div>
"""

    st.markdown(textwrap.dedent(exec_html), unsafe_allow_html=True)

    # =========================
    # STEP 6: HUMAN DECISION
    # =========================
    st.markdown('<div class="section-title">6 · Human Decision</div>', unsafe_allow_html=True)

    b1,b2,b3 = st.columns(3)
    with b1:
        if st.button("Review Evidence", use_container_width=True):
            st.info("Evidence view: indicators and synthetic supporting signals used by the agents.")
    with b2:
        if st.button("Explore Further", use_container_width=True):
            st.info("Ask another question or select another scenario to continue the booth journey.")
    with b3:
        if st.button("Acknowledge for Review", type="primary", use_container_width=True):
            st.success("Acknowledged for human operational review. No automated operational action has been executed.")

st.markdown('<div class="footer">Synthetic demonstration data only · No real patient, facility, or Ministry of Health operational data is used.</div>', unsafe_allow_html=True)
