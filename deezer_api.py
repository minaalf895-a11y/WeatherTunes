import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DEEZER_BASE_URL", "https://api.deezer.com")

def get_music_recommendation(mood):
    """
    Searches Deezer for a track and returns the direct link.
    """
    # Use the /search/track endpoint for better song results
    url = f"{BASE_URL}/search/track"
    # Append 'song' to your mood to get better music matches
    params = {"q": f"{mood} song", "limit": 1}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Ensure we actually got data back
        if "data" in data and len(data["data"]) > 0:
            track = data["data"][0]
            # This returns the direct URL to the song
            return track['link']
        else:
            return "No song found for this mood."
            
    except Exception as e:
        return f"Error connecting to Deezer: {e}"