import os
from dotenv import load_dotenv


# Use an absolute path to the file
env_path = r"C:\Users\This PC\Desktop\Spotify_Project\.env"

# Load the file specifically
load_dotenv(dotenv_path=env_path)

# Print current environment variables to see what's loaded
api_key = os.getenv("Weather_API_Key")

print(f"DEBUG: Looking for file at {env_path}")
print(f"DEBUG: API Key value is '{api_key}'")

if api_key:
    print("Success!")
else:
    print("Failure: Still None.")