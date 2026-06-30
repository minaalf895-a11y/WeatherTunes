import streamlit as st
from weather import get_weather
from deezer_api import get_music_recommendation

# 1. Page Configuration
st.set_page_config(
    page_title="Weather Mood Music | Your Sound, Your Vibe", 
    page_icon="🌤️", 
    layout="wide" # Use 'wide' layout to match the reference grid 
)

# 2. Dynamic Weather/Mood Mapping
MOOD_MAP = {
    "Clear": {"label": "HAPPY", "icon": "😊", "theme": "#FFC107"}, # Happy
    "Clouds": {"label": "CHILL", "icon": "😌", "theme": "#607D8B"}, # Chill
    "Rain": {"label": "RELAX", "icon": "🌧️", "theme": "#2196F3"}, # Relax
    "Drizzle": {"label": "PEACEFUL", "icon": "☔", "theme": "#8BC34A"}, # Peaceful
    "Thunderstorm": {"label": "ENERGETIC", "icon": "⚡", "theme": "#E91E63"}, # Energetic
    "Snow": {"label": "COZY", "icon": "❄️", "theme": "#9C27B0"}, # Cozy
    "Mist": {"label": "CALM", "icon": "🌫️", "theme": "#00BCD4"}, # Calm
    "Fog": {"label": "CALM", "icon": "🌫️", "theme": "#00BCD4"}, # Calm
    "Haze": {"label": "DREAMY", "icon": "🌅", "theme": "#F44336"}, # Dreamy
    "Atmosphere": {"label": "NEUTRAL", "icon": "🙂", "theme": "#757575"},
}
DEFAULT_MOOD = {"label": "NEUTRAL", "icon": "🙂", "theme": "#757575"}

# 3. Enhanced CSS for dynamic themes and professional UI
st.markdown(f"""
<style>
/* Main body styling and dynamic background gradient */
.stApp {{
    background: linear-gradient(135deg, #1A1A2E, #16213E, #0F3460);
    color: #FFFFFF;
    font-family: 'Poppins', sans-serif;
}}

/* Custom titles and headers */
.main-title {{
    color: #1DB954; 
    text-align: center; 
    font-size: 3rem !important; 
    font-weight: bold;
    margin-bottom: 20px;
    text-transform: uppercase;
}}
.sidebar .stText, .sidebar .stSubheader {{ color: #FFFFFF !important; }}

/* Input and buttons styling */
div.stTextInput>div>div>input {{
    background-color: #333333; 
    color: white !important; 
    border-radius: 20px; 
    border: 1px solid #1DB954; 
    padding: 10px;
}}
div.stButton>button {{
    background-color: #1DB954; 
    color: white; 
    border-radius: 20px; 
    width: 100%; 
    border: none; 
    font-weight: bold; 
    height: 3em;
    font-size: 1.1rem;
}}
div.stButton>button:hover {{
    background-color: #1ed760; 
    border: 1px solid white;
}}

/* Custom Cards (Mood panel, Track suggestions) */
.card {{
    background-color: #222222;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    border-left: 5px solid #1DB954;
}}
.card h2 {{ font-size: 1.5rem; }}

/* Deezer direct link button */
.listen-button {{
    display: block; 
    width: 100%; 
    text-align: center; 
    background-color: #FFFFFF; 
    color: #121212 !important; 
    border-radius: 20px; 
    padding: 15px; 
    font-weight: bold; 
    text-decoration: none !important;
    font-size: 1.2rem;
    margin-top: 15px;
    transition: 0.3s;
}}
.listen-button:hover {{
    background-color: #1DB954;
    color: white !important;
    transform: scale(1.05);
}}

/* Dynamic Mood Card styling based on mapped theme */
.dynamic-mood-card {{
    background-color: #222222;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    text-align: center;
}}
.mood-label {{ font-size: 1.8rem; font-weight: bold; margin-bottom: 10px; }}
.mood-icon {{ font-size: 3rem; margin-top: 15px; }}

</style>
""", unsafe_allow_html=True)

# 4. Main App Structure
st.markdown("<h1 class='main-title'>🌤️ Weather Mood Music</h1>", unsafe_allow_html=True)

# Define the grid layout to replicate the multi-panel reference
col1, col2 = st.columns([1, 2], gap="medium")

# Initialize city (using Lahore as default, since it's the requested location context)
if 'last_city' not in st.session_state:
    st.session_state['last_city'] = "Lahore"
if 'weather_data' not in st.session_state:
    st.session_state['weather_data'] = None

# PANEL 1: Input and Information (Sidebar Column)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Your Location")
    
    city_input = st.text_input("Enter city name:", placeholder="e.g., Lahore", value=st.session_state['last_city'])
    
    # Use standard Streamlit columns inside the container
    submit_col1, submit_col2 = st.columns([2, 1])
    
    search_type = submit_col1.selectbox("Recommendation type:", ["track", "playlist"])
    
    if submit_col2.button("Suggest Music", key="main_search"):
        if city_input:
            st.session_state['last_city'] = city_input
            with st.spinner('Checking the weather...'):
                st.session_state['weather_data'] = get_weather(city_input)
                # Reset music data when city changes
                if 'track_data' in st.session_state:
                    del st.session_state['track_data']
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state['weather_data']:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Current Weather")
        st.write(f"**City:** {st.session_state['weather_data']['City']}")
        st.write(f"**Condition:** {st.session_state['weather_data']['Condition']}")
        st.write(f"**Description:** {st.session_state['weather_data']['Description']}")
        st.markdown('</div>', unsafe_allow_html=True)

# PANEL 2 & 3: Results (Main Column)
with col2:
    w_data = st.session_state['weather_data']
    if w_data:
        # Determine mood from weather condition
        w_condition = w_data['Condition']
        mood_details = MOOD_MAP.get(w_condition, DEFAULT_MOOD)
        
        # Structure results grid: Mood on top, Track below
        res_col_left, res_col_right = st.columns([1, 1.5], gap="large")
        
        # Results PANEL A: Dynamic Mood Card
        with res_col_left:
            st.markdown(f"""
            <div class="dynamic-mood-card" style="border-top: 10px solid {mood_details['theme']}">
                <div class="mood-label" style="color: {mood_details['theme']}">{mood_details['label']}</div>
                <div class="mood-icon">{mood_details['icon']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Results PANEL B: Music Recommendation
        with res_col_right:
            mood_label = mood_details['label'].lower()
            
            # Use cached track data to avoid repeated API calls
            if 'track_data' not in st.session_state or st.session_state.get('search_type') != search_type:
                with st.spinner(f"Finding perfect {search_type} for your {mood_label} vibe..."):
                    st.session_state['track_data'] = get_music_recommendation(mood_label, search_type)
                    st.session_state['search_type'] = search_type
            
            track_title, artist_name, deezer_link = st.session_state['track_data']
            
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            st.write(f"**Now Recommending:** {'A Song' if search_type == 'track' else 'A Playlist'}")
            st.write(f"### {track_title}")
            st.write(f"**by {artist_name}**")
            
            # The 'Listen on Deezer' button uses the direct playable link
            st.markdown(f'<a href="{deezer_link}" target="_blank" class="listen-button">Listen on Deezer</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card" style="text-align: center;">', unsafe_allow_html=True)
        st.subheader("Welcome to WeatherTunes")
        st.write("Enter your city and click 'Suggest Music' to experience music tailored to your environment.")
        st.markdown('</div>', unsafe_allow_html=True)