import requests
from config.config import BASE_URLS

def fetch_soil_data(lat, lon):
    url = BASE_URLS["esa_worldcover"]
    response = requests.get(f"{url}/{lat}/{lon}")
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch soil data"}

def fetch_weather_data(lat, lon):
    url = BASE_URLS["open_meteo"]
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m,precipitation"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch weather data"}

def fetch_climate_data(lat, lon):
    url = BASE_URLS["nasa_power"]
    params = {"latitude": lat, "longitude": lon, "parameters": "T2M,PRECTOT", "format": "JSON"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch climate data"}
