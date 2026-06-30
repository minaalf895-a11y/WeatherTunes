import streamlit as st
from weather import get_weather
from deezer_api import get_music_recommendation

st.set_page_config(
    page_title="Weather Mood Music | Your Sound, Your Vibe",
    page_icon="🌤️",
    layout="wide"
)


MOOD_MAP = {
    "Clear": {"label": "HAPPY", "icon": "😊", "theme": "#FFC107"},
    "Clouds": {"label": "CHILL", "icon": "😌", "theme": "#607D8B"},
    "Rain": {"label": "RELAX", "icon": "🌧️", "theme": "#2196F3"},
    "Drizzle": {"label": "PEACEFUL", "icon": "☔", "theme": "#8BC34A"},
    "Thunderstorm": {"label": "ENERGETIC", "icon": "⚡", "theme": "#E91E63"},
    "Snow": {"label": "COZY", "icon": "❄️", "theme": "#9C27B0"},
    "Mist": {"label": "CALM", "icon": "🌫️", "theme": "#00BCD4"},
    "Fog": {"label": "CALM", "icon": "🌫️", "theme": "#00BCD4"},
    "Haze": {"label": "DREAMY", "icon": "🌅", "theme": "#F44336"},
    "Atmosphere": {"label": "NEUTRAL", "icon": "🙂", "theme": "#757575"},
}
DEFAULT_MOOD = {"label": "NEUTRAL", "icon": "🙂", "theme": "#757575"}
WEATHER_EMOJI = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️", "Mist": "🌫️", "Fog": "🌫️", "Haze": "🌅", "Atmosphere": "🌫️"}

st.markdown("""<style>.stApp { background: linear-gradient(135deg, #cfe9fb 0%, #eaf6ff 50%, #fdf6e3 100%); font-family: 'Poppins', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.glass-card { background: rgba(255,255,255,0.55); border-radius: 20px; padding: 24px; backdrop-filter: blur(10px); box-shadow: 0 8px 24px rgba(31, 41, 55, 0.08); margin-bottom: 20px; }
.card-label { font-weight: 700; font-size: 0.85rem; color: #374151; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
</style>""", unsafe_allow_html=True)


if 'last_city' not in st.session_state: st.session_state['last_city'] = "Lahore"
if 'weather_data' not in st.session_state: st.session_state['weather_data'] = None
if 'recent_cities' not in st.session_state: st.session_state['recent_cities'] = []
if 'mood_history' not in st.session_state: st.session_state['mood_history'] = []

sidebar_col, main_col = st.columns([1, 2.6], gap="medium")

with sidebar_col:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    city_input = st.text_input("Enter city name:", value=st.session_state['last_city'])
    search_type = st.selectbox("Recommendation type:", ["track", "playlist"])
    
    if st.button("Get Weather & Music"):
        st.session_state['last_city'] = city_input
        st.session_state['weather_data'] = get_weather(city_input)
        
        if 'track_data' in st.session_state: del st.session_state['track_data']


with main_col:
    w_data = st.session_state['weather_data']
    if w_data:
        w_condition = w_data.get('Condition', 'Atmosphere')
        mood_details = MOOD_MAP.get(w_condition, DEFAULT_MOOD)
        
        
        if 'track_data' not in st.session_state or st.session_state.get('search_type') != search_type:
            st.session_state['track_data'] = get_music_recommendation(mood_details['label'].lower(), search_type)
            st.session_state['search_type'] = search_type

       
        if 'track_data' in st.session_state:
            track_title, artist_name, deezer_link = st.session_state['track_data']
            
            st.success(f"Playing: {track_title}")
    else:
        st.info("Please enter a city and click the button to start.")
