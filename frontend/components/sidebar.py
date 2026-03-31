import streamlit as st
import os


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style='padding: 1rem 0 0.5rem'>
            <div style='font-family: Playfair Display, serif; font-size: 1.3rem; color: #f0a500;'>✈️ Smart Travel</div>
            <div style='font-size: 0.78rem; color: #8b949e; margin-top: 0.2rem;'>Multi-agent AI planner</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='font-size:0.8rem; color:#8b949e; margin-bottom:0.5rem'>AGENTS</div>", unsafe_allow_html=True)

        agents = [
            ("✈️", "Logistics Specialist", "Finds flights & routes"),
            ("🗺️", "Destination Scout",    "Attractions & hidden gems"),
            ("🌤️", "Weather Analyst",      "Weather & packing tips"),
            ("🎩", "Travel Concierge",     "Builds the final itinerary"),
        ]
        for icon, name, desc in agents:
            st.markdown(f"""
            <div class='agent-row'>
                <span style='font-size:1.1rem'>{icon}</span>
                <div>
                    <div class='agent-name'>{name}</div>
                    <div style='font-size:0.75rem; color:#8b949e'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='font-size:0.8rem; color:#8b949e; margin-bottom:0.8rem'>API STATUS</div>", unsafe_allow_html=True)

        api_keys = {
            "🤖 Groq LLM":       "GROQ_API_KEY",
            "🔍 Serper Search":  "SERPER_API_KEY",
            "🌦️ OpenWeather":    "OPENWEATHER_API_KEY",
            "📍 Foursquare":     "FOURSQUARE_API_KEY",
            "🛫 Aviationstack":  "AVIATIONSTACK_API_KEY",
        }
        for label, key in api_keys.items():
            dot = "🟢" if os.getenv(key) else "🔴"
            st.markdown(
                f"<div style='font-size:0.82rem; color:#c9d1d9; margin-bottom:0.3rem'>{dot} {label}</div>",
                unsafe_allow_html=True
            )
