import streamlit as st
import datetime
from backend.tools.flight_tool import get_flights, get_all_cities, city_to_iata
from backend.tools.weather_tool import get_weather

# --- 1. PERFORMANCE OPTIMIZATION (Caching) ---
# This prevents re-running logic every time a user clicks a button
@st.cache_data
def cached_cities():
    return get_all_cities()

@st.cache_data
def cached_iata(city_name):
    if not city_name: return "—"
    try:
        return city_to_iata(city_name)
    except Exception:
        return "???"

# --- 2. MAIN RENDER FUNCTION ---
def render():
    st.markdown("<div class='card'><h4>Quick Preview</h4><p>Search flights or check weather instantly.</p></div>", unsafe_allow_html=True)
    
    # Using tabs for a clean navigation experience
    t1, t2 = st.tabs(["✈️  Flights", "🌤️  Weather"])
    
    with t1:
        _render_flights()
    with t2:
        _render_weather()

# --- 3. FLIGHTS SECTION ---
def _render_flights():
    cities = cached_cities()
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Departure City</div>", unsafe_allow_html=True)
        dep = st.selectbox("dep", [""] + cities, key="qp_dep", label_visibility="collapsed")
    with c2:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Destination City</div>", unsafe_allow_html=True)
        dst = st.selectbox("dst", [""] + cities, key="qp_dst", label_visibility="collapsed")

    c3, c4 = st.columns([1, 1])
    with c3:
        st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>Travel Date</div>", unsafe_allow_html=True)
        date = st.date_input(
            "date", 
            value=datetime.date.today() + datetime.timedelta(days=7), 
            min_value=datetime.date.today(), 
            key="qp_date", 
            label_visibility="collapsed"
        )
    with c4:
        dc = cached_iata(dep)
        ac = cached_iata(dst)
        st.markdown(
            f"<div style='margin-top:1.6rem;padding:.55rem .9rem;background:#21262d;border-radius:8px;font-size:.82rem;color:#8b949e'>"
            f"IATA: <span style='color:#f0a500;font-weight:600'>{dc}</span> → "
            f"<span style='color:#f0a500;font-weight:600'>{ac}</span></div>", 
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # State Management: Check if we already have results to display
    if st.button("🔍  Search Flights", key="qp_search", use_container_width=True):
        if not dep or not dst:
            st.warning("Please select both cities.")
        elif dep == dst:
            st.warning("Cities must be different.")
        else:
            with st.spinner(f"Searching {dep} to {dst}..."):
                try:
                    result = get_flights(dep, dst, str(date))
                    st.session_state['flight_result'] = result
                except Exception as e:
                    st.error(f"Search failed: {e}")

    # Display results if they exist in session state
    if 'flight_result' in st.session_state:
        st.markdown(f"<div class='result-box'>{st.session_state['flight_result']}</div>", unsafe_allow_html=True)
        
        # Link Generation
        oi, di = cached_iata(dep), cached_iata(dst)
        gf_url = f"https://www.google.com/flights?q=flights+from+{oi}+to+{di}"
        # Skyscanner usually expects YYYYMMDD or YYYY-MM-DD
        ss_url = f"https://www.skyscanner.net/transport/flights/{oi.lower()}/{di.lower()}/{date.strftime('%Y%m%d')}/"
        
        st.markdown(f"""
            <div style='margin-top:1rem;display:flex;gap:.8rem'>
                <a href='{gf_url}' target='_blank' class='btn-primary' style='padding:.45rem 1.2rem;background:linear-gradient(135deg,#f0a500,#e07b00);color:#0d1117;border-radius:6px;font-size:.85rem;font-weight:600;text-decoration:none'>Google Flights ↗</a>
                <a href='{ss_url}' target='_blank' style='padding:.45rem 1.2rem;background:#21262d;border:1px solid #30363d;color:#c9d1d9;border-radius:6px;font-size:.85rem;font-weight:600;text-decoration:none'>Skyscanner ↗</a>
            </div>
        """, unsafe_allow_html=True)

# --- 4. WEATHER SECTION ---
def _render_weather():
    cities = cached_cities()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.85rem;color:#8b949e;margin-bottom:.3rem;font-weight:500'>City</div>", unsafe_allow_html=True)
    city = st.selectbox("wcity", [""] + cities, key="qp_wcity", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🌤️  Check Weather", key="qp_wbtn", use_container_width=True):
        if not city:
            st.warning("Please select a city.")
        else:
            with st.spinner(f"Fetching weather for {city}..."):
                try:
                    result = get_weather(city)
                    st.session_state['weather_result'] = result
                except Exception as e:
                    st.error(f"Weather check failed: {e}")

    if 'weather_result' in st.session_state:
         st.markdown(f"<div class='result-box'>{st.session_state['weather_result']}</div>", unsafe_allow_html=True)