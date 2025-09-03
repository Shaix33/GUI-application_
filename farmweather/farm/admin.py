from django.contrib import admin
from django.utils.html import format_html
from .models import Crop, Location, UserProfile, WeatherData
from .services import OpenMeteoService
import datetime

weather_service = OpenMeteoService()

# Crop admin
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'planting_season')
    search_fields = ('name', 'category')
    list_filter = ('category', 'planting_season')

# Location admin
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'user', 'is_primary')
    search_fields = ('name',)
    list_filter = ('is_primary',)

# UserProfile admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')

# WeatherData admin
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('location', 'recorded_at', 'temperature_current', 'precipitation', 'weather_code', 'fetch_latest')
    search_fields = ('location__name',)
    list_filter = ('weather_code', 'recorded_at')
    
    def fetch_latest(self, obj):
        """
        Display a button/link to fetch latest weather for this location
        """
        return format_html(
            '<a class="button" href="{}">Fetch Now</a>',
            f"/admin/farm/weatherdata/fetch/{obj.id}/"
        )
    fetch_latest.short_description = "Fetch Latest Weather"
    fetch_latest.allow_tags = True

# Register models
admin.site.register(Crop, CropAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WeatherData, WeatherDataAdmin)
