from django.shortcuts import render
from django.contrib import messages
from .forms import LocationForm
from .services import OpenMeteoService
from .crops import suggest_crops
import requests
import datetime

weather_service = OpenMeteoService()

def summarize_forecast(forecast):
    """Summarize OpenMeteo daily forecast (avg temp + total rainfall)."""
    if not forecast or "days" not in forecast:
        return None
    
    temps = []
    rain = 0
    for day in forecast["days"]:
        if day["temperature_max"] and day["temperature_min"]:
            temps.append((day["temperature_max"] + day["temperature_min"]) / 2)
        rain += day.get("precipitation_sum", 0) or 0
    
    return {
        "avg_temp": sum(temps)/len(temps) if temps else None,
        "total_rain_mm": rain
    }

def home(request):
    form = LocationForm(request.POST or None)
    context = {"form": form, "weather": None, "summary": None, "crops": [], "daily": []}

    if request.method == "POST" and form.is_valid():
        loc = form.cleaned_data["location"].strip()
        try:
            # TODO: use geocoding service to resolve loc → lat/lon
            # For now hardcode Pretoria as test
            lat, lon = -25.7461, 28.1881  

            current = weather_service.get_current_weather(lat, lon)
            forecast = weather_service.get_weather_forecast(lat, lon, days=7)
            summary = summarize_forecast(forecast)

            crops = suggest_crops(
                avg_temp=summary["avg_temp"] if summary else None,
                total_rain_mm=summary["total_rain_mm"] if summary else None
            )

            context.update({
                "weather": current,
                "summary": summary,
                "crops": crops,
                "daily": forecast.get("days", []) if forecast else [],
                "location_label": loc,  # later: use geocoding API
            })

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                messages.error(request, "Location not found. Try another city or a city ID (e.g., 990930).")
            else:
                messages.error(request, f"Weather service error: {e.response.status_code}")
        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")

    return render(request, "farm/home.html", context)


def check_box(request):
    return render(request, "farm/click.html")

def login_page(request):
    return render(request, "farm/login.html")
