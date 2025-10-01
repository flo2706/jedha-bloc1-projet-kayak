"""
Geocoding Extract — Nominatim (async)

Summary
- Fetch GPS coordinates (latitude/longitude) for a fixed list of French cities
  using the OpenStreetMap Nominatim API, with controlled concurrency and retries.

Inputs
- cities.json  (list of city names)

Outputs
- coordinates.json  (mapping: city -> {latitude, longitude} or {error})

Workflow
1) Load city names from JSON.
2) Query Nominatim concurrently (semaphore, retries, 429 handling).
3) Persist results as formatted JSON (UTF-8).

Config
- USER_AGENT (env var or default string) — required by Nominatim.
- MAX_CONCURRENT_REQUESTS — limit parallel requests.
- RETRIES — retry attempts per city.
"""

import aiohttp
import asyncio
import json
import logging
from typing import Tuple, Dict, Union
import os

# ---- Consistent paths: JSON files live next to this script ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "cities.json")        # input list of cities
OUTPUT_FILE = os.path.join(BASE_DIR, "coordinates.json")  # output coordinates

HEADERS = {
    # Nominatim requires a valid User-Agent (ideally with contact email/app name)
    "User-Agent": os.getenv("USER_AGENT", "KayakTripPlanner/1.0 (your_email@example.com)")
}
MAX_CONCURRENT_REQUESTS = 5
RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

async def get_coordinates(session: aiohttp.ClientSession, city: str, semaphore: asyncio.Semaphore) -> Tuple[str, Dict[str, Union[str, None]]]:
    """
    Query Nominatim for one city (with concurrency limit + retries).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}

    async with semaphore:
        for attempt in range(RETRIES):
            try:
                async with session.get(url, params=params, headers=HEADERS, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            return city, {"latitude": data[0]["lat"], "longitude": data[0]["lon"]}
                        return city, {"latitude": None, "longitude": None}
                    if response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 5))
                        logger.warning(f"{city} - Too many requests. Waiting {retry_after}s.")
                        await asyncio.sleep(retry_after)
                        continue
                    return city, {"error": f"HTTP {response.status}"}
            except Exception as e:
                logger.error(f"[attempt {attempt+1}/{RETRIES}] {city} - Exception: {e}")
                await asyncio.sleep(1)
    return city, {"error": "Failed after multiple attempts"}

def load_cities(filepath: str) -> list:
    """Load cities from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_results(filepath: str, data: dict):
    """Persist coordinates dict as JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f"Data saved to {filepath}")

async def fetch_all_coordinates(cities: list[str]) -> dict:
    """Fetch coordinates concurrently for all cities."""
    results = {}
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = [get_coordinates(session, city, semaphore) for city in cities]
        for future in asyncio.as_completed(tasks):
            city, coords = await future
            results[city] = coords
            logger.info(f"{city} → {coords}")
    return results

async def main():
    """1) load cities, 2) fetch coords, 3) save results."""
    cities = load_cities(INPUT_FILE)
    coordinates = await fetch_all_coordinates(cities)
    save_results(OUTPUT_FILE, coordinates)

if __name__ == "__main__":
    asyncio.run(main())
