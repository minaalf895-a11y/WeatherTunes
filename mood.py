def detect_mood(condition):
    """
    Convert weather condition into a mood.
    """

    mood_map = {
        "Clear": "Happy 😊",
        "Clouds": "Chill 😌",
        "Rain": "Relax 🌧️",
        "Drizzle": "Peaceful ☔",
        "Thunderstorm": "Energetic ⚡",
        "Snow": "Cozy ❄️",
        "Mist": "Calm 🌫️",
        "Fog": "Calm 🌫️",
        "Smoke": "Focus 🎧",
        "Haze": "Dreamy 🌅",
        "Dust": "Adventure 🚗",
        "Sand": "Adventure 🏜️",
        "Ash": "Reflective 🤔",
        "Squall": "Power 💪",
        "Tornado": "Intense 🔥"
    }

    return mood_map.get(condition, "Neutral 🙂")