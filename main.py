import os
from dotenv import load_dotenv

# Load the .env file from the project root (works on any machine/OS,
# unlike a hardcoded absolute Windows path)
load_dotenv()

# Use the same env var name as weather.py / deezer_api.py expect
api_key = os.getenv("WEATHER_API_KEY")

print(f"DEBUG: API Key value is '{api_key}'")

if api_key:
    print("Success!")
else:
    print("Failure: WEATHER_API_KEY not found. Check your .env file.")
