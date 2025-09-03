import requests
from django.conf import settings
from  django.core.cache import cache
from datetime import datetime, timedelta
import logging
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class OpenMeteoService:

    def __init__(self):
        self.base_url = settings.OPENMETEO_BASE_URL
        self.geocoding_url = settings.GEOCODING_API_URL

    def get_current_weather(self, latitude: float, longitude: float) -> dict:

        try:
            url = f"{self.base_url}/forecast"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current' : [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'apparent_temperature',
                    'is_day',
                    'precipitation',
                    'weather_code',
                    'cloud_cover',
                    'pressure_msl',
                    'surface_pressure',
                    'wind_speed_10m',
                    'wind_direction_10m',
                    'wind_gusts_10m',
                ],
                'timezone': 'auto',
                'forecast_days': 1,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data.get('current', {})
            return {
                'temperature': current.get('temperature_2m'),
                'humidity': current.get('relative_humidity_2m'),
                'surface_pressure': current.get('surface_pressure'),
                'apparent_temperature': current.get('apparent_temperature'),
                'is_day': current.get('is_day') == 1,
                'precipitation': current.get('precipitation'),
                'weather_code': current.get('weather_code'),
                'cloud_cover': current.get('cloud_cover'),
                'pressure': current.get('pressure_msl') or current.get('surface_pressure'),
                'wind_speed': current.get('wind_speed_10m'),
                'wind_direction': current.get('wind_direction_10m'),
                'wind_gusts': current.get('wind_gusts_10m'),
                'timezone': data.get('timezone'),
                'elevation': data.get('elevation'),
                'time': current.get('time'),
            }
        except requests.RequestException as e:
                    logger.error(f"Error fetching current weather: {e}")
                    return None
        except Exception as e:
            logger.error(f"Weather data processing error: {e}")
            return None
        
        
    def get_weather_forecast(self, latitude: float, longitude: float, days: int = 7) -> dict:
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'apparent_temperature_max',
                    'apparent_temperature_min',
                    'precipitation_sum',
                    'precipitation_probability_max',
                    'weather_code',
                    'cloud_cover_mean',
                    'windspeed_10m_max',
                    'windgusts_10m_max',
                    'wind_direction_10m_dominant',
                    'uv_index_max',
                ],
                'timezone': 'auto',
                'forecast_days': min(days, 16),
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            daily = data.get('daily', {})
            dates = daily.get('time', [])

            forecast_data = {
                'timezone': data.get('timezone'),
                'elevation': data.get('elevation'),
                'days': []
            }
            

            for i, date_str in enumerate(dates):
                day_data = {
                    'date': date_str,
                    'temperature_max': daily.get('temperature_2m_max', [None]*len(dates))[i],
                    'temperature_min': daily.get('temperature_2m_min', [None]*len(dates))[i],
                    'apparent_temperature_max': daily.get('apparent_temperature_max', [None]*len(dates))[i],
                    'apparent_temperature_min': daily.get('apparent_temperature_min', [None]*len(dates))[i],
                    'precipitation_sum': daily.get('precipitation_sum', [0]*len(dates))[i],
                    'precipitation_probability': daily.get('precipitation_probability_max', [0]*len(dates))[i],
                    'weather_code': daily.get('weather_code', [None]*len(dates))[i],
                    'cloud_cover_mean': daily.get('cloud_cover_mean', [None]*len(dates))[i],
                    'wind_speed_max': daily.get('windspeed_10m_max', [None]*len(dates))[i],
                    'wind_gusts_max': daily.get('windgusts_10m_max', [None]*len(dates))[i],
                    'wind_direction': daily.get('wind_direction_10m_dominant', [None]*len(dates))[i],
                    'uv_index': daily.get('uv_index_max', [None]*len(dates))[i]
                }
                forecast_data['days'].append(day_data)

            return forecast_data
        
        except requests.RequestException as e:
            logger.error(f"Error fetching weather forecast: {e}")
            return None
        except Exception as e:
            logger.error(f"Forecast data processing error: {e}")
            return None
    
    def get_historical_weather(self, latitude: float, longitude: float, start_date, end_date) -> dict | None:
    
        try:
            url = f"{self.base_url}/archive"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'daily': [
                    'weather_code',
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'wind_speed_10m_max'
                ],
                'timezone': 'auto'
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            daily = data.get('daily', {})
            dates = daily.get('time', [])

            historical_data = {
                'timezone': data.get('timezone', 'UTC'),
                'elevation': data.get('elevation', 0),
                'days': []
            }

            for i, date_str in enumerate(dates):
                day_data = {
                    'date': date_str,
                    'weather_code': daily.get('weather_code', [None]*len(dates))[i],
                    'temperature_max': daily.get('temperature_2m_max', [None]*len(dates))[i],
                    'temperature_min': daily.get('temperature_2m_min', [None]*len(dates))[i],
                    'precipitation_sum': daily.get('precipitation_sum', [0]*len(dates))[i],
                    'wind_speed_max': daily.get('wind_speed_10m_max', [None]*len(dates))[i]
                }
                historical_data['days'].append(day_data)

            return historical_data

        except requests.RequestException as e:
            logger.error(f"OpenMeteo historical weather API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Historical weather data processing error: {e}")
            return None
        
