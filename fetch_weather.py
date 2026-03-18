import requests
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

cities = [
    {"name": "Vancouver", "country": "CA"},
    {"name": "Dhahran", "country": "SA"},
    {"name": "Jakarta", "country": "ID"}
]

def fetch_weather(city, country):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    return {
        "city": city,
        "country": country,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }

for city in cities:
    weather = fetch_weather(city["name"], city["country"])
    supabase.table("weather_data").insert(weather).execute()
    print(f"Saved weather for {city['name']}: {weather['temperature']}°C, {weather['condition']}")