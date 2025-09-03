from .mapmycrop_service import fetch_crop_monitoring_data
from .weather_service import fetch_weather_data
from .climate_classifier import classify_climate, generate_crops

def get_crop_recommendations(location):
    lat = location.get("lat")
    lon = location.get("lon")
    name = location.get("name", "Unknown")

    weather = fetch_weather_data(location)
    temp = weather.get("temperature")
    rainfall = weather.get("rainfall")

    zone = classify_climate(temp, rainfall)
    rule_based_crops = generate_crops(zone)

    satellite_data = fetch_crop_monitoring_data(lat, lon)
    crop_health = satellite_data.get("crop_health")

    return {
        "location": name,
        "climate_zone": zone,
        "recommended_crops": rule_based_crops,
        "crop_health": crop_health,
        "satellite_timestamp": satellite_data.get("timestamp")
    }