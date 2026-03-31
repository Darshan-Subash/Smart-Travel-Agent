import streamlit as st


def render():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### 🏗️ Architecture")
        st.markdown("""
        <div class='card'>
        <p>
        <b style='color:#f0a500'>SmartTravelCrew</b> orchestrates four CrewAI agents
        running sequentially on <b>Groq's LLaMA-3 70B</b> model.
        <br><br>
        ✈️ <b>Logistics Specialist</b> — Aviationstack + Serper<br>
        🗺️ <b>Destination Scout</b> — Foursquare + Serper<br>
        🌤️ <b>Weather Analyst</b> — OpenWeatherMap + Serper<br>
        🎩 <b>Travel Concierge</b> — synthesises the final plan
        </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### 📁 Folder Structure")
        st.code("""smart_travel_agent/
├── backend/
│   ├── agents/
│   │   └── travel_agents.py
│   ├── tasks/
│   │   └── travel_tasks.py
│   ├── tools/
│   │   ├── flight_tool.py
│   │   ├── places_tool.py
│   │   ├── search_tool.py
│   │   └── weather_tool.py
│   └── crew.py
├── frontend/
│   ├── components/
│   │   ├── agent_status.py
│   │   ├── sidebar.py
│   │   └── styles.py
│   └── pages/
│       ├── about.py
│       ├── plan_trip.py
│       └── quick_preview.py
├── output/itineraries/
├── data/knowledge/
├── app.py
├── main.py
├── .env
└── requirements.txt""", language="text")

    with col2:
        st.markdown("#### 🔑 Required API Keys")
        st.markdown("""
        <div class='card'>
        <p>
        Add these to your <code>.env</code> file:<br><br>
        <b style='color:#f0a500'>GROQ_API_KEY</b><br>
        <span style='color:#8b949e; font-size:0.82rem'>console.groq.com — free tier available</span><br><br>
        <b style='color:#f0a500'>SERPER_API_KEY</b><br>
        <span style='color:#8b949e; font-size:0.82rem'>serper.dev — 2500 free searches/month</span><br><br>
        <b style='color:#f0a500'>OPENWEATHER_API_KEY</b><br>
        <span style='color:#8b949e; font-size:0.82rem'>openweathermap.org — free tier</span><br><br>
        <b style='color:#f0a500'>FOURSQUARE_API_KEY</b><br>
        <span style='color:#8b949e; font-size:0.82rem'>developer.foursquare.com — free tier</span><br><br>
        <b style='color:#f0a500'>AVIATIONSTACK_API_KEY</b><br>
        <span style='color:#8b949e; font-size:0.82rem'>aviationstack.com — free tier</span>
        </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### ▶️ Run the App")
        st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

        st.markdown("#### 💻 CLI Mode")
        st.code("python main.py", language="bash")
