from datetime import datetime, timedelta
import pytz

def get_weather_description(weather_code):
    """Convert OpenMeteo weather code to description"""
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return descriptions.get(weather_code, "Unknown")

def get_weather_emoji(weather_code):
    """Convert OpenMeteo weather code to emoji"""
    emojis = {
        0: '☀️',      
        1: '🌤️',      
        2: '⛅',      
        3: '☁️',      
        45: '🌫️',     
        48: '🌫️',     
        51: '🌦️',     
        53: '🌦️',     
        55: '🌦️',     
        61: '🌧️',     
        63: '🌧️',     
        65: '🌧️',     
        80: '🌦️',     
        81: '🌧️',     
        82: '⛈️',     
        95: '⛈️',     
        96: '⛈️',     
        99: '⛈️',     
    }
    return emojis.get(weather_code, '🌤️')

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def get_time_based_greeting(current_time):
    """Get greeting based on time of day"""
    hour = current_time.hour
    
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

def get_user_timezone(user):
    """Get user's timezone from their primary location"""
    try:
        profile = user.userprofile
        if profile.primary_location and profile.primary_location.timezone:
            return pytz.timezone(profile.primary_location.timezone)
    except:
        pass
    return pytz.UTC

def calculate_growing_season_score(crop, current_date, location_timezone):
    """Calculate if it's the right season for planting"""
    # Convert to local timezone
    local_date = current_date.astimezone(location_timezone)
    month = local_date.month

    season_months = {
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'autumn': [9, 10, 11],
        'winter': [12, 1, 2],
        'year_round': list(range(1, 13))
    }

    crop_months = season_months.get(crop.planting_season, [])

    if not crop_months:
        return 0.0  # Unknown or unsupported season

    if month in crop_months:
        return 1.0  # Ideal planting time

    # Check proximity to ideal months (±1 month)
    proximity = min(abs(month - m) if abs(month - m) <= 6 else 12 - abs(month - m) for m in crop_months)
    if proximity == 1:
        return 0.5  # Near ideal

    return 0.0  # Not suitable