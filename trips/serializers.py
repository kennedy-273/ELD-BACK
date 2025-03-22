from rest_framework import serializers
from .models import DriverProfile, Trip, LogSheet
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DriverProfile
        fields = ['id', 'user', 'name']

class LogSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSheet
        fields = ['id', 'date', 'duty_status', 'start_time', 'end_time', 'location']

class TripSerializer(serializers.ModelSerializer):
    logs = LogSheetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = ['id', 'current_location', 'pickup_location', 'dropoff_location', 'current_cycle_used', 
                  'current_lat', 'current_lng', 'pickup_lat', 'pickup_lng', 'dropoff_lat', 'dropoff_lng', 
                  'transport_type', 'created_at', 'logs']

