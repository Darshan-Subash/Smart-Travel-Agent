import streamlit as st
import datetime

# --- 1. BACKEND IMPORTS ---
try:
    from backend.crew import SmartTravelCrew
    from backend.tools.flight_tool import get_all_cities
except ImportError:
    st.error("Backend modules not found. Ensure 'backend' folder is in your root directory.")

def render():
    # Cache city loading to keep UI snappy
    cities = get_all_cities() if 'get_all_cities' in globals() else []
    
    st.markdown("<div class='card'><h4>Plan My Trip</h4><p>Our AI crew builds your full itinerary.</p></div>", unsafe_allow_html=True)
    
    # --- Input Grid (Columns 1-8) ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Departure City</div>", unsafe_allow_html=True)
        origin = st.selectbox("ori", [""] + cities, key="pt_ori", label_visibility="collapsed")
    with c2:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Destination City</div>", unsafe_allow_html=True)
        dest = st.selectbox("dst", [""] + cities, key="pt_dst", label_visibility="collapsed")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Departure Date</div>", unsafe_allow_html=True)
        date = st.date_input("date", value=datetime.date.today() + datetime.timedelta(days=14), 
                            min_value=datetime.date.today(), key="pt_date", label_visibility="collapsed")
    with c4:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Duration (days)</div>", unsafe_allow_html=True)
        dur = st.number_input("dur", min_value=1, max_value=30, value=7, key="pt_dur", label_visibility="collapsed")

    c5, c6 = st.columns(2)
    with c5:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Budget</div>", unsafe_allow_html=True)
        budget = st.selectbox("bud", ["budget", "mid-range", "luxury"], index=1, key="pt_bud", label_visibility="collapsed")
    with c6:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Travel Style</div>", unsafe_allow_html=True)
        style = st.selectbox("sty", ["adventure", "cultural", "relaxation", "balanced", "family", "business"], 
                             index=3, key="pt_sty", label_visibility="collapsed")

    c7, c8 = st.columns(2)
    with c7:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Travellers</div>", unsafe_allow_html=True)
        travelers = st.number_input("trv", min_value=1, max_value=20, value=2, key="pt_trv", label_visibility="collapsed")
    with c8:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Interests (optional)</div>", unsafe_allow_html=True)
        interests = st.text_input("int", placeholder="e.g. food, history, beaches", key="pt_int", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 2. EXECUTION LOGIC ---
    if st.button("🗺️  Plan My Trip", key="pt_go", use_container_width=True):
        # Structured validation (better than 'return' inside the function)
        if not origin or not dest:
            st.warning("Please select both a departure and destination city.")
        elif origin == dest:
            st.warning("Departure and destination cities must be different.")
        else:
            with st.spinner("AI crew planning your trip..."):
                try:
                    # Run the Crew
                    crew = SmartTravelCrew()
                    result = crew.run(
                        origin=origin, 
                        destination=dest, 
                        duration=dur,
                        depart_date=str(date), 
                        budget=budget, 
                        travel_style=style,
                        travelers=travelers, 
                        interests=interests,
                    )
                    
                    # Store result in session state to persist through re-runs
                    st.session_state['itinerary'] = getattr(result, "raw", str(result))
                    
                except Exception as e:
                    st.error(f"Planning failed: {e}")
                    st.info("Tip: Check your API keys in your .env file.")

    # --- 3. PERSISTENT RESULT DISPLAY ---
    if 'itinerary' in st.session_state:
        st.markdown("---")
        st.markdown(f"<div class='result-box'>{st.session_state['itinerary']}</div>", unsafe_allow_html=True)