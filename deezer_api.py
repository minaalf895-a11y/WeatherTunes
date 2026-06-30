import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("DEEZER_BASE_URL", "https://api.deezer.com")


def get_music_recommendation(mood, type="track"):
    """
    Searches Deezer for a track or playlist matching the mood.
    """
  
    query = f"{mood} Pakistani Hindi {type}"
    url = f"{BASE_URL}/search/{type}"
    params = {"q": query, "limit": 1}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            item = data["data"][0]
           
            if type == "track":
                return (item['title'], item['artist']['name'], item['link'])
            elif type == "playlist":
                return (item['title'], "Various Artists", item['link'])
        
        return (f"{mood.capitalize()} Vibe", "Deezer", "https://www.deezer.com")
    except Exception as e:
        return (f"Error", "Deezer", "https://www.deezer.com")
