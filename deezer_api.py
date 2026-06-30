import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("DEEZER_BASE_URL", "https://api.deezer.com")

def get_music_recommendation(mood, type="track"):
    """Searches Deezer for a track or playlist matching the mood."""
    query = f"{mood} Pakistani Hindi {type}"
    url = f"{BASE_URL}/search/{type}"
    params = {"q": query, "limit": 1}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            item = data["data"][0]
            if type == "track":
                return (item.get('title', 'Unknown'), item['artist'].get('name', 'Unknown'), item.get('link', 'https://www.deezer.com'))
            elif type == "playlist":
                return (item.get('title', 'Unknown'), "Various Artists", item.get('link', 'https://www.deezer.com'))
        
        return (f"{mood.capitalize()} Vibe", "Deezer", "https://www.deezer.com")
    except Exception:
        return ("Vibe", "Deezer", "https://www.deezer.com")
