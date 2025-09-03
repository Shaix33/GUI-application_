from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
import json

class Location(models.Model):
    """User location with OpenMeteo integration"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2, default='')
    timezone = models.CharField(max_length=50, default='UTC')
    elevation = models.FloatField(null=True, blank=True)  # OpenMeteo provides this
    
    # Location metadata
    is_primary = models.BooleanField(default=False)
    detected_automatically = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['user', 'is_primary']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure only one primary location per user
        if self.is_primary:
            Location.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def get_cache_key(self, data_type='current'):
        """Generate cache key for weather data"""
        return f"weather:{data_type}:{self.latitude}:{self.longitude}"
    
    def get_current_weather(self):
        """Fetch current weather from OpenMeteo with caching"""
        cache_key = self.get_cache_key('current')
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        
        from .services import OpenMeteoService
        weather_service = OpenMeteoService()
        weather_data = weather_service.get_current_weather(self.latitude, self.longitude)
        
        if weather_data:
            # Cache for 10 minutes
            cache.set(cache_key, json.dumps(weather_data), 600)
        
        return weather_data
    
    def get_weather_forecast(self, days=7):
        """Get weather forecast for next N days"""
        cache_key = self.get_cache_key(f'forecast_{days}')
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)
        
        from .services import OpenMeteoService
        weather_service = OpenMeteoService()
        forecast_data = weather_service.get_weather_forecast(
            self.latitude, self.longitude, days
        )
        
        if forecast_data:
            # Cache forecast for 30 minutes
            cache.set(cache_key, json.dumps(forecast_data), 1800)
        
        return forecast_data
    
    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"

class WeatherData(models.Model):
    """Store historical weather data from OpenMeteo"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='weather_history')
    
    # Basic weather data
    temperature_current = models.FloatField()
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    humidity = models.FloatField()
    pressure = models.FloatField(null=True, blank=True)
    
    # Wind data
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    wind_gusts = models.FloatField(null=True, blank=True)
    
    # Precipitation
    precipitation = models.FloatField(default=0)  # mm
    precipitation_probability = models.FloatField(null=True, blank=True)
    
    # Weather conditions
    weather_code = models.IntegerField()  # OpenMeteo weather code
    weather_description = models.CharField(max_length=100)
    cloud_cover = models.FloatField(null=True, blank=True)
    visibility = models.FloatField(null=True, blank=True)
    uv_index = models.FloatField(null=True, blank=True)
    
    # Timestamps
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['location', 'recorded_at']
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['location', 'recorded_at']),
            models.Index(fields=['weather_code']),
        ]
    
    def get_weather_emoji(self):
        """Convert OpenMeteo weather code to emoji"""
        weather_emojis = {
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
        return weather_emojis.get(self.weather_code, '🌤️')

class Crop(models.Model):
    """Enhanced crop model for farming recommendations"""
    SOIL_TYPES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loam', 'Loam'),
        ('silt', 'Silt'),
        ('peaty', 'Peaty'),
        ('chalky', 'Chalky'),
    ]
    
    SEASONS = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('year_round', 'Year Round'),
    ]
    
    # Basic info
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=50)  
    
    # Growing conditions (aligned with OpenMeteo data)
    optimal_temp_min = models.FloatField(help_text="Minimum temperature in Celsius")
    optimal_temp_max = models.FloatField(help_text="Maximum temperature in Celsius")
    optimal_rainfall_min = models.FloatField(help_text="Minimum rainfall in mm/month")
    optimal_rainfall_max = models.FloatField(help_text="Maximum rainfall in mm/month")
    
    # Soil requirements
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    soil_ph_min = models.FloatField(default=6.0)
    soil_ph_max = models.FloatField(default=7.5)
    
    # Weather sensitivity
    frost_tolerance = models.BooleanField(default=False)
    drought_tolerance = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    wind_tolerance = models.BooleanField(default=True)
    
    # Growing timeline
    planting_season = models.CharField(max_length=20, choices=SEASONS)
    days_to_germination = models.IntegerField(default=7)
    days_to_maturity = models.IntegerField()
    harvest_duration_days = models.IntegerField(default=30)
    
    # Spacing and care
    spacing_cm = models.IntegerField(help_text="Plant spacing in centimeters")
    water_frequency_days = models.IntegerField(default=3)
    fertilizer_schedule = models.TextField(blank=True)
    
    # Additional data
    companion_plants = models.ManyToManyField('self', blank=True, symmetrical=False)
    common_pests = models.TextField(blank=True)
    common_diseases = models.TextField(blank=True)
    growing_tips = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['planting_season']),
        ]
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile for farming data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Farm details
    farm_name = models.CharField(max_length=100, blank=True)
    farm_size_hectares = models.FloatField(null=True, blank=True)
    farming_experience = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner (0-2 years)'),
        ('intermediate', 'Intermediate (3-10 years)'),
        ('experienced', 'Experienced (10+ years)'),
    ], default='beginner')
    
    # Location preferences
    primary_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    
    # Crop preferences
    preferred_crops = models.ManyToManyField(Crop, blank=True)
    farming_methods = models.JSONField(default=dict, help_text="organic, conventional, etc.")
    
    # Notification settings
    weather_alerts = models.BooleanField(default=True)
    planting_reminders = models.BooleanField(default=True)
    harvest_reminders = models.BooleanField(default=True)
    
    # Display preferences
    temperature_unit = models.CharField(max_length=10, choices=[
        ('celsius', 'Celsius'),
        ('fahrenheit', 'Fahrenheit')
    ], default='celsius')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"