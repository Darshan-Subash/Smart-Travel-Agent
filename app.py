import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Smart Travel Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from frontend.components.styles import inject_styles
from frontend.components.sidebar import render_sidebar
import frontend.pages.plan_trip as plan_trip
import frontend.pages.quick_preview as quick_preview
import frontend.pages.about as about

# Apply global styles
inject_styles()

# Sidebar
render_sidebar()

# Hero
st.markdown("""
<div class='hero'>
    <h1>Smart <span>Travel</span> Agent</h1>
    <p>Four AI agents. One perfect itinerary.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Tabs — each tab delegates to its own page module
tab1, tab2, tab3 = st.tabs(["🗺️  Plan My Trip", "🔍  Quick Preview", "ℹ️  About"])

with tab1:
    plan_trip.render()

with tab2:
    quick_preview.render()

with tab3:
    about.render()
