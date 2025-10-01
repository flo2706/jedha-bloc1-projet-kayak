"""
Weather Extract — OpenWeather One Call 3.0

Summary
- Fetch a 7-day daily forecast for each city from `coordinates.json`
  and write a raw, tidy CSV for downstream processing.

Inputs
- coordinates.json  (city -> {latitude, longitude})
- OPENWEATHER_API_KEY (env var)

Outputs
- weather_7_day_forecast.csv  (one row = city × day, UTF-8)
"""

import requests
import csv
import json
from datetime import datetime, UTC
import os
from dotenv import load_dotenv

# Configuration 
load_dotenv()  # Load environment variables from a .env file (OPENWEATHER_API_KEY, etc.)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Paths: everything stays in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input: coordinates file lives in coordGPS/
COORDS_FILE = os.path.join(BASE_DIR, "../coordGPS/coordinates.json")

# Output: CSV saved directly next to this script
OUTPUT_CSV  = os.path.join(BASE_DIR, "weather_7_day_forecast.csv")

# Load city coordinates (lat/lon) 
try:
    with open(COORDS_FILE, "r", encoding="utf-8") as file:
        cities = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading coordinates: {e}")
    exit()

# Open CSV and write header once 
with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'city', 'date', 'temp_min', 'temp_max', 'temp_feels_like', 'humidity', 'pressure',
        'wind_speed', 'wind_gust', 'wind_deg', 'clouds', 'uvi', 'dew_point', 'pop',
        'sunrise', 'sunset', 'moon_phase', 'conditions'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each city and call OpenWeather One Call 3.0 
    for city_name, coords in cities.items():
        try:
            lat = float(coords["latitude"])
            lon = float(coords["longitude"])

            url = (
                "https://api.openweathermap.org/data/3.0/onecall"
                f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=en"
            )

            response = requests.get(url, timeout=20)
            data = response.json()

            if response.status_code == 200 and "daily" in data:
                for day in data["daily"][:7]:  # limit to 7 days
                    date    = datetime.fromtimestamp(day["dt"], UTC).strftime('%Y-%m-%d')
                    sunrise = datetime.fromtimestamp(day["sunrise"], UTC).strftime('%H:%M:%S')
                    sunset  = datetime.fromtimestamp(day["sunset"],  UTC).strftime('%H:%M:%S')

                    row = {
                        'city': city_name,
                        'date': date,
                        'temp_min': day["temp"]["min"],
                        'temp_max': day["temp"]["max"],
                        'temp_feels_like': day["feels_like"]["day"],
                        'humidity': day["humidity"],
                        'pressure': day["pressure"],
                        'wind_speed': day["wind_speed"],
                        'wind_gust': day.get("wind_gust", "N/A"),
                        'wind_deg': day["wind_deg"],
                        'clouds': day["clouds"],
                        'uvi': day["uvi"],
                        'dew_point': day["dew_point"],
                        'pop': day["pop"],
                        'sunrise': sunrise,
                        'sunset': sunset,
                        'moon_phase': day["moon_phase"],
                        'conditions': day["weather"][0]["description"]
                    }
                    writer.writerow(row)
            else:
                print(f"API error for {city_name}: {data}")

        except Exception as e:
            print(f"Error for {city_name}: {e}")

print(f"Weather data successfully saved to {OUTPUT_CSV}")
