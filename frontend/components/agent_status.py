import streamlit as st


AGENTS = [
    ("✈️", "Logistics Specialist"),
    ("🗺️", "Destination Scout"),
    ("🌤️", "Weather Analyst"),
    ("🎩", "Travel Concierge"),
]

STEP_STATUSES = {
    0: ("waiting", "waiting", "waiting", "waiting"),
    1: ("running", "waiting", "waiting", "waiting"),
    2: ("done",    "running", "waiting", "waiting"),
    3: ("done",    "done",    "running", "waiting"),
    4: ("done",    "done",    "done",    "running"),
    5: ("done",    "done",    "done",    "done"),
}


def render_agent_status(placeholder, step: int):
    statuses = STEP_STATUSES.get(step, STEP_STATUSES[0])
    rows = ""
    for (icon, name), status in zip(AGENTS, statuses):
        dot = "● " if status == "running" else ""
        rows += f"""
        <div class='agent-row'>
            <span style='font-size:1.1rem'>{icon}</span>
            <span class='agent-name'>{name}</span>
            <span class='badge badge-{status}'>{dot}{status.capitalize()}</span>
        </div>"""
    placeholder.markdown(f"<div class='card'>{rows}</div>", unsafe_allow_html=True)
