import os
import requests
from dotenv import load_dotenv
from mood import detect_mood

# Load the .env file
load_dotenv()

# Get API key
api_key = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    if api_key is None:
        print("❌ ERROR: WEATHER_API_KEY not found in .env file.")
        return None

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url)

        if response.status_code != 200:
            data = response.json()
            print("❌ Error:", data.get("message", "Something went wrong."))
            return None

        data = response.json()

        weather_data = {
            "City": data["name"],
            "Temperature": f'{data["main"]["temp"]} °C',
            "Feels Like": f'{data["main"]["feels_like"]} °C',
            "Humidity": f'{data["main"]["humidity"]}%',
            "Condition": data["weather"][0]["main"],
            "Description": data["weather"][0]["description"].title(),
            "Wind Speed": f'{data["wind"]["speed"]} m/s',
            "Mood": detect_mood(data["weather"][0]["main"]) 
        }

        return weather_data

    except requests.exceptions.RequestException as e:
        print("❌ Network Error:", e)
        return None


# ---------------- MAIN PROGRAM ---------------- #
# Only runs when this file is executed directly (e.g. `python weather.py`),
# NOT when it's imported by app.py — otherwise Streamlit would hang/crash
# every time it tries to import get_weather(), since input() has no stdin
# to read from in a Streamlit process.

if __name__ == "__main__":
    city = input("Enter city name: ")

    weather = get_weather(city)

    if weather:
        print("\n========== WEATHER REPORT ==========\n")

        for key, value in weather.items():
            print(f"{key:<15}: {value}")
