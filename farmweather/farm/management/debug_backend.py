from django.core.management.base import BaseCommand
from farm.services import OpenMeteoService
from farm.models import Crop, Location, WeatherData
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Debug and test backend services and models'

    def handle(self, *args, **options):
        self.stdout.write("=== Backend Debug Script ===")

        # 1️⃣ Test OpenMeteoService
        self.stdout.write("Testing OpenMeteoService...")
        service = OpenMeteoService()
        lat, lon = -25.7461, 28.1881  # Pretoria

        current = service.get_current_weather(lat, lon)
        if current:
            self.stdout.write(f"Current weather: {current}")
        else:
            self.stdout.write("Failed to fetch current weather!")

        forecast = service.get_weather_forecast(lat, lon, days=7)
        if forecast:
            self.stdout.write(f"7-day forecast: {forecast}")
        else:
            self.stdout.write("Failed to fetch forecast!")

        # 2️⃣ Test Models
        self.stdout.write("Testing Models...")

        crop_count = Crop.objects.count()
        self.stdout.write(f"Crops in DB: {crop_count}")
        if crop_count == 0:
            self.stdout.write("Creating test crop...")
            Crop.objects.create(name="Test Maize", category="Grain", planting_season="Spring")
            self.stdout.write(f"New Crops in DB: {Crop.objects.count()}")

        location_count = Location.objects.count()
        self.stdout.write(f"Locations in DB: {location_count}")

        weather_count = WeatherData.objects.count()
        self.stdout.write(f"WeatherData entries in DB: {weather_count}")

        # 3️⃣ Test Historical Weather
        self.stdout.write("Testing historical weather...")
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        historical = service.get_historical_weather(lat, lon, start_date, end_date)
        if historical:
            self.stdout.write(f"Historical weather: {historical}")
        else:
            self.stdout.write("Failed to fetch historical weather!")

        self.stdout.write("=== Backend Debug Complete ===")
