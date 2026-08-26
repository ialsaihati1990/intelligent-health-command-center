import streamlit as st
import pandas as pd
import numpy as np
import textwrap
import time
from pathlib import Path
import base64

st.set_page_config(page_title='Intelligent Health Command Center', page_icon='🧠', layout='wide', initial_sidebar_state='collapsed')

NAVY='#1B365D'; CYAN='#00A3E0'; TEAL='#007681'; BG='#F4F7F9'
LOGO_PATH=Path('assets/moh_nhcc_logo.png')

def html(x):
    st.markdown(textwrap.dedent(x).strip(), unsafe_allow_html=True)

def goto(n):
    st.session_state.stage=n
    st.rerun()

def restart():
    st.session_state.stage=0
    st.session_state.scenario=None
    st.rerun()

if 'stage' not in st.session_state: st.session_state.stage=0
if 'scenario' not in st.session_state: st.session_state.scenario=None

@st.cache_data
def demo_data(seed=26):
    rng=np.random.default_rng(seed)
    zones=['Central','North','East','West']
    rows=[]
    for i in range(1,13):
        rows.append({
            'Facility':f'Facility {i:02d}', 'Zone':zones[(i-1)%4],
            'ED Wait (min)':int(np.clip(rng.normal(105,28),45,220)),
            'Bed Occupancy (%)':round(float(np.clip(rng.normal(84,8),55,99)),1),
            'LOS (days)':round(float(np.clip(rng.normal(4.7,1.15),2.2,9)),1),
            'Lab TAT (min)':int(np.clip(rng.normal(72,19),30,160)),
            'Discharge Delays':int(np.clip(rng.normal(16,6),3,35)),
            'Critical Lab Alerts':int(np.clip(rng.normal(6,3),0,16)),
        })
    df=pd.DataFrame(rows)
    df.loc[df['Facility']=='Facility 07',['ED Wait (min)','Bed Occupancy (%)','LOS (days)','Discharge Delays']]=[188,97.2,7.8,31]
    df.loc[df['Facility']=='Facility 03',['ED Wait (min)','Bed Occupancy (%)','LOS (days)']]=[164,94.5,6.9]
    df.loc[df['Facility']=='Facility 10',['Lab TAT (min)','Critical Lab Alerts']]=[143,13]
    return df

def risk_table(df):
    z=df.copy()
    z['Risk Score']=(
        .30*np.clip((z['ED Wait (min)']-90)/100,0,1)+
        .25*np.clip((z['Bed Occupancy (%)']-80)/20,0,1)+
        .20*np.clip((z['LOS (days)']-4)/5,0,1)+
        .15*np.clip((z['Lab TAT (min)']-60)/100,0,1)+
        .10*np.clip((z['Discharge Delays']-10)/25,0,1)
    )*100
    return z.sort_values('Risk Score',ascending=False)

df=demo_data(); risk_df=risk_table(df)

SCENARIOS={
    'Emergency Department Pressure':{'icon':'🚑','desc':'Detect rising ED pressure and connect it to downstream capacity constraints.','question':'Which facilities show the highest ED operational pressure today?'},
    'Bed Capacity & Patient Flow':{'icon':'🛏️','desc':'Identify capacity bottlenecks and patient-flow constraints.','question':'Where are bed capacity and patient flow most constrained?'},
    'Laboratory Performance':{'icon':'🧪','desc':'Surface delayed turnaround times and critical laboratory signals.','question':'Which facilities need attention for laboratory performance?'},
    'Cross-Service Operational Risk':{'icon':'🧠','desc':'Connect multiple operational signals into one prioritized executive view.','question':'Which facility needs attention first, and what is driving the risk?'},
}

if LOGO_PATH.exists():
    b64=base64.b64encode(LOGO_PATH.read_bytes()).decode()
    logo=f'<img src="data:image/png;base64,{b64}" style="max-width:100%;max-height:110px;object-fit:contain;">'
else:
    logo='<div style="color:#1B365D;font-weight:900;text-align:center;font-size:19px">Ministry of Health<br>+<br>NHCC</div>'

st.markdown(f'''
<style>
.stApp{{background:linear-gradient(180deg,#F9FBFC 0%,{BG} 100%);}}
[data-testid="stHeader"]{{background:transparent;}}
[data-testid="stToolbar"],#MainMenu,footer{{visibility:hidden;}}
.block-container{{max-width:1500px;padding-top:.6rem;padding-bottom:2rem;}}
.hero{{background:linear-gradient(115deg,#102B4A 0%,{NAVY} 55%,{TEAL} 100%);border-radius:28px;padding:24px 28px;color:white;box-shadow:0 18px 42px rgba(27,54,93,.18);}}
.hero-grid{{display:grid;grid-template-columns:220px 1fr 270px;gap:26px;align-items:center;}}
.logo{{background:white;border-radius:20px;padding:14px;min-height:125px;display:flex;align-items:center;justify-content:center;}}
.kicker{{color:#BEEBFA;font-size:12px;letter-spacing:.15em;font-weight:900;}}
.title{{font-size:42px;font-weight:900;line-height:1.05;margin:7px 0;}}
.sub{{font-size:18px;color:#DDEEF4;line-height:1.4;}}
.demo{{background:rgba(4,45,67,.48);border:1px solid rgba(255,255,255,.2);border-radius:17px;padding:14px;font-size:12px;line-height:1.5;}}
.steps{{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:17px 0 24px;}}
.step{{background:white;border:1px solid #DFE8ED;border-radius:15px;padding:12px;color:#6B7883;font-size:12px;font-weight:800;}}
.step.active{{background:linear-gradient(120deg,{TEAL},{NAVY});color:white;border-color:transparent;}}
.step.done{{background:#ECF7F2;color:{TEAL};border-color:#BFE3D2;}}
.screen{{background:white;border:1px solid #DFE8ED;border-radius:26px;padding:28px;box-shadow:0 14px 34px rgba(27,54,93,.07);min-height:500px;}}
.k{{color:{TEAL};font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;}}
.h1{{color:{NAVY};font-size:34px;line-height:1.1;font-weight:900;margin:7px 0 8px;}}
.p{{color:#687680;font-size:15px;line-height:1.5;margin-bottom:20px;}}
.bigq{{font-size:42px;line-height:1.15;font-weight:900;color:{NAVY};max-width:930px;margin:38px auto 18px;text-align:center;}}
.tag{{color:{TEAL};font-size:19px;font-weight:800;text-align:center;margin-bottom:24px;}}
.scbox{{background:linear-gradient(120deg,#fff,#F3FBFD);border:1px solid #DCE8ED;border-radius:22px;padding:22px;}}
.chip{{display:inline-block;padding:6px 10px;background:#ECF8FB;color:{TEAL};border-radius:999px;font-size:11px;font-weight:900;margin:4px;}}
.agents{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0 16px;}}
.agent{{background:white;border:1px solid #DDE8ED;border-radius:19px;padding:18px;text-align:center;box-shadow:0 8px 18px rgba(27,54,93,.05);}}
.dot{{width:44px;height:44px;margin:0 auto 10px;border-radius:50%;background:linear-gradient(135deg,{CYAN},{TEAL});box-shadow:0 0 0 8px rgba(0,163,224,.07);}}
.agent b{{color:{NAVY};font-size:14px;}} .agent small{{display:block;color:{TEAL};margin-top:5px;}}
.super{{background:linear-gradient(120deg,{TEAL},{NAVY});color:white;border-radius:19px;padding:17px;text-align:center;font-size:16px;font-weight:900;}}
.exec{{background:white;border-radius:24px;padding:24px;box-shadow:0 14px 35px rgba(27,54,93,.09);border-top:6px solid {TEAL};}}
.pri{{display:inline-block;padding:6px 11px;border-radius:999px;background:#FDEBEB;color:#B42318;border:1px solid #F8B4B4;font-size:12px;font-weight:900;}}
.row{{display:grid;grid-template-columns:48px 1fr;gap:12px;padding:15px 0;border-bottom:1px dashed #DDE5EA;}}
.ico{{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px solid #9FD5DD;color:{TEAL};}}
.lab{{color:{TEAL};font-size:12px;font-weight:900;text-transform:uppercase;}} .txt{{color:{NAVY};font-size:16px;line-height:1.45;margin-top:3px;}}
.pill{{display:inline-block;background:#EEF3F7;color:{NAVY};border-radius:10px;padding:7px 10px;margin:3px 4px 0 0;font-size:12px;font-weight:800;}}
.human{{background:{NAVY};color:white;border-radius:18px;padding:18px;text-align:center;font-size:20px;font-weight:900;margin-top:16px;}}
div.stButton>button{{border-radius:14px;min-height:48px;font-weight:850;}}
@media(max-width:900px){{.hero-grid{{grid-template-columns:1fr}}.steps{{grid-template-columns:1fr 1fr}}.agents{{grid-template-columns:1fr 1fr}}}}
</style>
''',unsafe_allow_html=True)

html(f'''<div class="hero"><div class="hero-grid"><div class="logo">{logo}</div><div><div class="kicker">NATIONAL HEALTH COMMAND CENTER</div><div class="title">Intelligent Health Command Center</div><div class="sub">Powered by Agentic AI<br>From Real-Time Signals to Intelligent Decision Support</div></div><div class="demo"><b>DEMO DATA ONLY</b><br><br>All facility names, operational values, alerts, scores and recommendations are synthetically generated and do not represent real Ministry of Health data.</div></div></div>''')

labels=['Start','Scenario','Multi-Agent Analysis','Executive Intelligence','Human Decision']
parts=['<div class="steps">']
for i,label in enumerate(labels):
    cls='step done' if i<st.session_state.stage else ('step active' if i==st.session_state.stage else 'step')
    parts.append(f'<div class="{cls}">{i+1} · {label}</div>')
parts.append('</div>'); html(''.join(parts))

@st.dialog('Choose a Scenario', width='large')
def choose_scenario():
    st.markdown('### What would you like the Command Center to investigate?')
    st.caption('Select one scenario to begin the Agentic AI experience.')
    names=list(SCENARIOS)
    c1,c2=st.columns(2)
    for i,name in enumerate(names):
        with (c1 if i%2==0 else c2):
            meta=SCENARIOS[name]
            st.markdown(f"#### {meta['icon']} {name}")
            st.caption(meta['desc'])
            if st.button(f'Select {name}',key=f's{i}',use_container_width=True):
                st.session_state.scenario=name; st.session_state.stage=1; st.rerun()

if st.session_state.stage==0:
    html('''<div class="screen"><div class="k">Visitor Experience</div><div class="bigq">What would you like the Command Center to investigate?</div><div class="tag">Multi-Agent Intelligence · Connected Insights · Better Decisions</div><div style="max-width:900px;margin:auto;text-align:center;color:#6C7983;font-size:16px;line-height:1.6">Experience how a scalable Multi-Agent AI ecosystem analyzes operational signals, connects findings across domains, prioritizes what matters and supports informed human decision-making.</div></div>''')
    _,mid,_=st.columns([1,1.4,1])
    with mid:
        if st.button('Start Experience →',type='primary',use_container_width=True): choose_scenario()

elif st.session_state.stage==1:
    if not st.session_state.scenario: choose_scenario(); st.stop()
    name=st.session_state.scenario; meta=SCENARIOS[name]
    html(f'''<div class="screen"><div class="k">Selected Scenario</div><div class="scbox"><div style="font-size:42px">{meta['icon']}</div><div class="h1">{name}</div><div class="p">{meta['desc']}</div><span class="chip">Multi-Agent Ecosystem</span><span class="chip">Supervisor Agent</span><span class="chip">Human Oversight</span></div><div style="color:{TEAL};font-size:12px;font-weight:900;text-transform:uppercase;margin-top:18px">Command Center Question</div><div style="color:{NAVY};font-size:29px;font-weight:900;line-height:1.25;margin-top:6px">{meta['question']}</div></div>''')
    a,b,c=st.columns([1,1.5,1])
    with a:
        if st.button('← Change Scenario',use_container_width=True): choose_scenario()
    with b:
        if st.button('Run Multi-Agent Analysis →',type='primary',use_container_width=True): goto(2)
    with c:
        if st.button('Restart',use_container_width=True): restart()

elif st.session_state.stage==2:
    name=st.session_state.scenario
    html(f'''<div class="screen"><div class="k">Multi-Agent Analysis</div><div class="h1">{name}</div><div class="p">A scalable network of AI agents analyzes multiple operational domains in parallel. The Supervisor Agent then connects the findings and prioritizes operational impact.</div><div class="agents"><div class="agent"><div class="dot"></div><b>Operational Signals</b><small>Analyzing patterns…</small></div><div class="agent"><div class="dot"></div><b>Domain Intelligence</b><small>Evaluating context…</small></div><div class="agent"><div class="dot"></div><b>Cross-Service Connection</b><small>Connecting findings…</small></div><div class="agent"><div class="dot"></div><b>Priority Assessment</b><small>Assessing impact…</small></div></div><div class="super">🧠 Supervisor Agent · Connects · Reasons · Prioritizes</div></div>''')
    p=st.progress(0,text='Initializing Multi-Agent analysis...')
    for pct,msg in [(20,'Reading synthetic operational signals...'),(45,'Analyzing multiple operational domains...'),(68,'Connecting findings across services...'),(86,'Supervisor Agent assessing impact...'),(100,'Executive intelligence ready.')]:
        time.sleep(.22); p.progress(pct,text=msg)
    l,r=st.columns(2)
    with l:
        if st.button('← Back',use_container_width=True): goto(1)
    with r:
        if st.button('View Executive Intelligence →',type='primary',use_container_width=True): goto(3)

elif st.session_state.stage==3:
    name=st.session_state.scenario
    if name=='Emergency Department Pressure':
        rec=df.sort_values('ED Wait (min)',ascending=False).iloc[0]; facility=rec['Facility']
        situation=f'{facility} shows the highest ED pressure signal in the demonstration dataset.'
        why='ED waiting is occurring alongside high bed occupancy and extended length of stay, indicating a potential downstream patient-flow constraint.'
        drivers=[f"ED Wait {int(rec['ED Wait (min)'])} min",f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",f"LOS {rec['LOS (days)']:.1f} days"]
        action='Review patient flow, available capacity and discharge constraints with the responsible operational teams.'
    elif name=='Bed Capacity & Patient Flow':
        rec=df.sort_values(['Bed Occupancy (%)','LOS (days)'],ascending=False).iloc[0]; facility=rec['Facility']
        situation=f'{facility} shows the strongest combined bed-capacity and patient-flow constraint.'
        why='High occupancy is occurring together with prolonged LOS and delayed discharges, suggesting a potential patient-flow bottleneck.'
        drivers=[f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",f"LOS {rec['LOS (days)']:.1f} days",f"Delayed Discharges {int(rec['Discharge Delays'])}"]
        action='Review discharge readiness, bed turnover and upstream/downstream flow constraints with the responsible operational teams.'
    elif name=='Laboratory Performance':
        rec=df.sort_values('Lab TAT (min)',ascending=False).iloc[0]; facility=rec['Facility']
        situation=f'{facility} shows the highest laboratory turnaround time in the demonstration dataset.'
        why='Delayed turnaround combined with critical laboratory alerts may affect operational responsiveness and requires further validation.'
        drivers=[f"Lab TAT {int(rec['Lab TAT (min)'])} min",f"Critical Alerts {int(rec['Critical Lab Alerts'])}"]
        action='Review laboratory workflow, critical-result escalation and capacity conditions with the responsible operational teams.'
    else:
        rec=risk_df.iloc[0]; facility=rec['Facility']
        situation=f'{facility} is the highest-priority facility after connecting multiple operational signals across services.'
        why='The priority does not come from one KPI alone. It emerges from several operational signals occurring together.'
        drivers=[f"ED Wait {int(rec['ED Wait (min)'])} min",f"Occupancy {rec['Bed Occupancy (%)']:.1f}%",f"LOS {rec['LOS (days)']:.1f} days",f"Lab TAT {int(rec['Lab TAT (min)'])} min",f"Delayed Discharges {int(rec['Discharge Delays'])}"]
        action='Initiate a focused operational review, validate the evidence with responsible teams, and then determine the appropriate intervention.'
    pills=''.join([f'<span class="pill">{d}</span>' for d in drivers])
    html(f'''<div class="screen"><div class="k">Executive Intelligence</div><div class="exec"><span class="pri">HIGH PRIORITY</span><h2 style="color:{NAVY};font-size:35px;margin:14px 0 5px">{facility}</h2><div class="row"><div class="ico">⌁</div><div><div class="lab">What is happening?</div><div class="txt">{situation}</div></div></div><div class="row"><div class="ico">?</div><div><div class="lab">Why does it matter?</div><div class="txt">{why}</div></div></div><div class="row"><div class="ico">▥</div><div><div class="lab">Key Connected Drivers</div><div class="txt">{pills}</div></div></div><div class="row" style="border-bottom:none"><div class="ico">◎</div><div><div class="lab">Recommended Attention</div><div class="txt">{action}</div></div></div></div><div class="human">AI Recommends. Humans Decide. · Human-in-the-Loop</div></div>''')
    with st.expander('View synthetic supporting data'):
        st.dataframe(df,use_container_width=True,hide_index=True)
    l,r=st.columns(2)
    with l:
        if st.button('← Back to Analysis',use_container_width=True): goto(2)
    with r:
        if st.button('Continue to Human Decision →',type='primary',use_container_width=True): goto(4)

elif st.session_state.stage==4:
    html('''<div class="screen"><div class="k">Human Decision</div><div class="bigq" style="font-size:38px">AI Recommends. Humans Decide.</div><div class="tag">Human-in-the-Loop · Governed · Auditable</div><div style="max-width:900px;margin:auto;text-align:center;color:#687680;font-size:16px;line-height:1.6">Agentic AI supports the Command Center by connecting signals, surfacing priorities and generating decision intelligence. Final operational decisions remain under human review and accountability.</div></div>''')
    a,b,c=st.columns(3)
    with a:
        if st.button('Review Evidence',use_container_width=True): st.info('Synthetic evidence view: operational indicators and supporting signals used by the analysis.')
    with b:
        if st.button('Explore Another Scenario',use_container_width=True): st.session_state.stage=1; choose_scenario()
    with c:
        if st.button('Acknowledge for Review',type='primary',use_container_width=True): st.success('Acknowledged for human operational review. No automated operational action has been executed.')
    if st.button('Restart Visitor Experience',use_container_width=True): restart()
