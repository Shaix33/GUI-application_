# weather_service.py
from farmweather.services import OpenMeteoService

weather_service = OpenMeteoService()

def fetch_weather_data(location):
    lat = location.get("lat")
    lon = location.get("lon")
    return weather_service.get_current_weather(lat, lon)
