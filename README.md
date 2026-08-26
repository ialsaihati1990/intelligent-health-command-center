
# Intelligent Health Command Center — Booth UX Prototype

A Streamlit prototype for testing the visitor experience of an Agentic AI demonstration for the National Health Command Center.

## Important
All values, facility names, alerts, risk scores, and recommendations are synthetically generated for demonstration purposes. They do not represent real Ministry of Health data.

## Visitor journey
1. Choose a scenario
2. Ask the Command Center
3. Watch specialized agents analyze their domains
4. Supervisor Agent connects signals
5. Executive Intelligence Card is generated
6. Human decision / review remains in control

## Included scenarios
- Emergency Department Pressure
- Bed Capacity & Patient Flow
- Laboratory Performance
- Cross-Service Operational Risk

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## NHCC brand colors used
- Dark Cobalt Blue: #1B365D
- Cyan: #00A3E0
- Teal: #007681
- Apple Green: #64A70B
- Lime Green: #A9C23F

The logo asset in `assets/` was extracted from the user-provided NHCC PowerPoint template for use in this prototype.
