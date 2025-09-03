from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CropViewSet, LocationViewSet, WeatherDataViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'crops', CropViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'weather', WeatherDataViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),   # API endpoints
]
