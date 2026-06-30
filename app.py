import streamlit as st
from weather import get_weather
from deezer_api import get_music_recommendation

# 1. Page Configuration
st.set_page_config(
    page_title="Weather Mood Music | Your Sound, Your Vibe",
    page_icon="🌤️",
    layout="wide"
)

# 2. Dynamic Weather/Mood Mapping
MOOD_MAP = {
    "Clear":        {"label": "HAPPY",     "icon": "😊", "theme": "#FFC107"},
    "Clouds":       {"label": "CHILL",     "icon": "😌", "theme": "#607D8B"},
    "Rain":         {"label": "RELAX",     "icon": "🌧️", "theme": "#2196F3"},
    "Drizzle":      {"label": "PEACEFUL",  "icon": "☔", "theme": "#8BC34A"},
    "Thunderstorm": {"label": "ENERGETIC", "icon": "⚡", "theme": "#E91E63"},
    "Snow":         {"label": "COZY",      "icon": "❄️", "theme": "#9C27B0"},
    "Mist":         {"label": "CALM",      "icon": "🌫️", "theme": "#00BCD4"},
    "Fog":          {"label": "CALM",      "icon": "🌫️", "theme": "#00BCD4"},
    "Haze":         {"label": "DREAMY",    "icon": "🌅", "theme": "#F44336"},
    "Atmosphere":   {"label": "NEUTRAL",   "icon": "🙂", "theme": "#757575"},
}
DEFAULT_MOOD = {"label": "NEUTRAL", "icon": "🙂", "theme": "#757575"}

WEATHER_EMOJI = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️",
    "Thunderstorm": "⛈️", "Snow": "❄️", "Mist": "🌫️", "Fog": "🌫️",
    "Haze": "🌅", "Atmosphere": "🌫️",
}

# 3. CSS — light "frosted glass" theme matching the reference design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #cfe9fb 0%, #eaf6ff 50%, #fdf6e3 100%);
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

.app-title {
    font-weight: 800;
    font-size: 1.4rem;
    color: #14213d;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.section-label {
    font-weight: 700;
    font-size: 0.75rem;
    color: #6b7280;
    letter-spacing: 1px;
    margin: 18px 0 8px 0;
    text-transform: uppercase;
}
.sidebar-card {
    background: rgba(255,255,255,0.55);
    border-radius: 18px;
    padding: 18px;
    backdrop-filter: blur(6px);
}
.recent-item, .mood-item {
    background: rgba(255,255,255,0.6);
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 6px;
    font-size: 0.92rem;
    color: #1f2937;
}
.glass-card {
    background: rgba(255,255,255,0.55);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 24px rgba(31, 41, 55, 0.08);
    margin-bottom: 20px;
    height: 100%;
}
.card-label {
    font-weight: 700;
    font-size: 0.85rem;
    color: #374151;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.weather-temp { font-size: 3.2rem; font-weight: 800; color: #111827; line-height: 1; }
.weather-desc { font-size: 1.1rem; color: #374151; margin-top: 4px; }
.weather-emoji { font-size: 3.5rem; }

.mood-orb-wrap {
    display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;
}
.mood-orb {
    width: 150px; height: 150px; border-radius: 50%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-weight: 800; font-size: 1.15rem; color: #111827;
}
.track-art {
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 14px;
    background: linear-gradient(135deg, #ff6ec4, #7873f5, #4ade80, #facc15);
    background-size: 300% 300%;
    animation: gradientshift 8s ease infinite;
}
@keyframes gradientshift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.track-title { font-size: 1.5rem; font-weight: 800; color: #111827; margin-top: 4px;}
.track-artist { font-size: 1rem; color: #4b5563; }

.listen-button {
    display: block; width: 100%; text-align: center;
    background: linear-gradient(90deg, #1DB954, #2196F3);
    color: #ffffff !important;
    border-radius: 14px; padding: 16px; font-weight: 700;
    text-decoration: none !important; font-size: 1.05rem; transition: 0.25s;
}
.listen-button:hover { filter: brightness(1.08); transform: scale(1.02); }

.stat-card { background: rgba(255,255,255,0.6); border-radius: 14px; padding: 14px 16px; text-align: center; }
.stat-icon { font-size: 1.3rem; }
.stat-value { font-weight: 700; font-size: 1.05rem; color: #111827; }
.stat-label { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }

div.stTextInput>div>div>input {
    background-color: #ffffff; color: #111827 !important;
    border-radius: 12px; border: 1px solid #d1d5db; padding: 10px;
}
div.stButton>button {
    background: linear-gradient(90deg, #2196F3, #1DB954);
    color: white; border-radius: 12px; width: 100%;
    border: none; font-weight: 700; height: 2.8em;
}
div.stButton>button:hover { filter: brightness(1.08); }
</style>
""", unsafe_allow_html=True)

# 4. Session state setup
if 'last_city' not in st.session_state:
    st.session_state['last_city'] = "Lahore"
if 'weather_data' not in st.session_state:
    st.session_state['weather_data'] = None
if 'recent_cities' not in st.session_state:
    st.session_state['recent_cities'] = []
if 'mood_history' not in st.session_state:
    st.session_state['mood_history'] = []
if 'error' not in st.session_state:
    st.session_state['error'] = None

# 5. Layout: sidebar (left) + main content (right)
sidebar_col, main_col = st.columns([1, 2.6], gap="medium")

# ---------------- SIDEBAR ----------------
with sidebar_col:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown('<div class="app-title">🌤️ WEATHER MOOD<br/>MUSIC</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Enter City</div>', unsafe_allow_html=True)
    city_input = st.text_input(
        "Enter city name:",
        placeholder="e.g., Lahore",
        value=st.session_state['last_city'],
        label_visibility="collapsed",
    )
    search_type = st.selectbox("Recommendation type:", ["track", "playlist"], label_visibility="collapsed")

    if st.button("Get Weather & Music", key="main_search"):
        if city_input and city_input.strip():
            st.session_state['last_city'] = city_input
            st.session_state['error'] = None
            try:
                with st.spinner('Checking the weather...'):
                    weather_result = get_weather(city_input)

                # Some get_weather() implementations return None on failure
                # instead of raising — handle that case too.
                if not weather_result:
                    st.session_state['weather_data'] = None
                    st.session_state['error'] = f"Could not find weather for '{city_input}'. Check the city name."
                else:
                    st.session_state['weather_data'] = weather_result
                    if 'track_data' in st.session_state:
                        del st.session_state['track_data']

                    # Update recent cities (most recent first, unique, max 5)
                    rc = st.session_state['recent_cities']
                    rc = [c for c in rc if c.lower() != city_input.lower()]
                    rc.insert(0, city_input)
                    st.session_state['recent_cities'] = rc[:5]

                    # Update mood history
                    cond = weather_result.get('Condition', 'Atmosphere')
                    mood = MOOD_MAP.get(cond, DEFAULT_MOOD)
                    mh = st.session_state['mood_history']
                    mh.insert(0, {"mood": mood, "city": city_input})
                    st.session_state['mood_history'] = mh[:5]

            except Exception as e:
                st.session_state['weather_data'] = None
                st.session_state['error'] = f"Something went wrong fetching weather: {e}"
        else:
            st.session_state['error'] = "Please enter a city name."

    if st.session_state['recent_cities']:
        st.markdown('<div class="section-label">Recent Cities</div>', unsafe_allow_html=True)
        for c in st.session_state['recent_cities']:
            st.markdown(f'<div class="recent-item">{c}</div>', unsafe_allow_html=True)

    if st.session_state['mood_history']:
        st.markdown('<div class="section-label">Mood History</div>', unsafe_allow_html=True)
        for entry in st.session_state['mood_history']:
            m = entry["mood"]
            st.markdown(
                f'<div class="mood-item">{m["label"].title()} {m["icon"]} '
                f'<span style="color:#6b7280;">— {entry["city"]}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN CONTENT ----------------
with main_col:
    if st.session_state.get('error'):
        st.error(st.session_state['error'])

    w_data = st.session_state['weather_data']

    if w_data:
        w_condition = w_data.get('Condition', 'Atmosphere')
        mood_details = MOOD_MAP.get(w_condition, DEFAULT_MOOD)
        emoji = WEATHER_EMOJI.get(w_condition, "🌡️")

        temp = w_data.get('Temperature', w_data.get('Temp'))
        humidity = w_data.get('Humidity')
        wind = w_data.get('Wind', w_data.get('WindSpeed'))

        # Row 1: Weather card + Mood orb
        top_left, top_right = st.columns([1.6, 1], gap="medium")

        with top_left:
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-label">{w_data.get('City', city_input).upper()}</div>
                <div style="display:flex; align-items:center; gap:20px;">
                    <div class="weather-emoji">{emoji}</div>
                    <div>
                        <div class="weather-temp">{f"{temp}°C" if temp is not None else "—"}</div>
                        <div class="weather-desc">{str(w_data.get('Description', '')).title()}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with top_right:
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-label" style="text-align:center;">Detected Mood</div>
                <div class="mood-orb-wrap">
                    <div class="mood-orb" style="background: radial-gradient(circle, {mood_details['theme']}55, {mood_details['theme']}22);
                         box-shadow: 0 0 35px {mood_details['theme']}66;">
                        {mood_details['label']}<br/><span style="font-size:2rem;">{mood_details['icon']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Row 2: Now Playing card
        mood_label = mood_details['label'].lower()
        if 'track_data' not in st.session_state or st.session_state.get('search_type') != search_type:
            try:
                with st.spinner(f"Finding the perfect {search_type} for your {mood_label} vibe..."):
                    st.session_state['track_data'] = get_music_recommendation(mood_label, search_type)
                    st.session_state['search_type'] = search_type
            except Exception:
                st.session_state['track_data'] = (f"{mood_label.capitalize()} Vibe", "Deezer", "https://www.deezer.com")
                st.session_state['search_type'] = search_type

        track_title, artist_name, deezer_link = st.session_state['track_data']

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        np_label, np_link = st.columns([3, 1])
        with np_label:
            st.markdown('<div class="card-label">Now Playing</div>', unsafe_allow_html=True)
        with np_link:
            st.markdown(
                f'<div style="text-align:right;"><a href="{deezer_link}" target="_blank" '
                f'style="color:#1DB954; font-weight:700; text-decoration:none;">Feel Good Hits &gt;</a></div>',
                unsafe_allow_html=True,
            )

        art_col, info_col, btn_col = st.columns([1, 2, 1.4], gap="medium")
        with art_col:
            st.markdown('<div class="track-art"></div>', unsafe_allow_html=True)
        with info_col:
            subtitle = f"by {artist_name}" if artist_name else ("Mood Uplifters" if search_type == "track" else "Mood Playlist")
            st.markdown(f"""
                <div class="track-title">{track_title}</div>
                <div class="track-artist">{subtitle}</div>
            """, unsafe_allow_html=True)
        with btn_col:
            st.markdown(
                f'<a href="{deezer_link}" target="_blank" class="listen-button">🎧 Listen on Deezer</a>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Row 3: Stat mini-cards
        s1, s2, s3, s4 = st.columns(4, gap="medium")
        with s1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🌡️</div>
                <div class="stat-value">{f"{temp}°C" if temp is not None else "—"}</div>
                <div class="stat-label">Temperature</div>
            </div>""", unsafe_allow_html=True)
        with s2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">💧</div>
                <div class="stat-value">{f"{humidity}%" if humidity is not None else "—"}</div>
                <div class="stat-label">Humidity</div>
            </div>""", unsafe_allow_html=True)
        with s3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🌬️</div>
                <div class="stat-value">{f"{wind} km/h" if wind is not None else "—"}</div>
                <div class="stat-label">Wind</div>
            </div>""", unsafe_allow_html=True)
        with s4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{emoji}</div>
                <div class="stat-value">{w_condition}</div>
                <div class="stat-label">Condition</div>
            </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding: 60px 20px;">
            <div style="font-size:3rem;">🎧🌤️</div>
            <h2 style="color:#111827;">Welcome to WeatherTunes</h2>
            <p style="color:#4b5563; font-size:1.05rem;">
                Enter your city in the sidebar and click "Get Weather &amp; Music"<br/>
                to experience music tailored to your environment.
            </p>
        </div>
        """, unsafe_allow_html=True)
