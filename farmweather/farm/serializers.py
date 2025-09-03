from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Crop, Location, WeatherData, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class WeatherDataSerializer(serializers.ModelSerializer):
    weather_emoji = serializers.CharField(source="get_weather_emoji", read_only=True)
    class Meta:
        model = WeatherData
        fields = '__all__'

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'
