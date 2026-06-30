import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("DEEZER_BASE_URL", "https://api.deezer.com")


def get_music_recommendation(mood, type="track"):
    """Searches Deezer for a track or playlist matching the mood."""
    mood = mood or "chill"
    query = f"{mood} Pakistani Hindi {type}"
    url = f"{BASE_URL}/search/{type}"
    params = {"q": query, "limit": 1}

    try:
        response = requests.get(url, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            item = data["data"][0]
            if type == "track":
                title = item.get("title", "Unknown")
                artist_name = item.get("artist", {}).get("name", "Unknown")
                link = item.get("link", "https://www.deezer.com")
                return (title, artist_name, link)
            elif type == "playlist":
                title = item.get("title", "Unknown")
                link = item.get("link", "https://www.deezer.com")
                return (title, "Various Artists", link)

        return (f"{mood.capitalize()} Vibe", "Deezer", "https://www.deezer.com")

    except requests.exceptions.RequestException:
        # Network error, timeout, or bad HTTP status
        return (f"{mood.capitalize()} Vibe", "Deezer", "https://www.deezer.com")
    except (ValueError, KeyError):
        # Malformed JSON or unexpected response shape
        return (f"{mood.capitalize()} Vibe", "Deezer", "https://www.deezer.com")
