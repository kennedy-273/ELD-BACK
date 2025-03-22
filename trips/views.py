from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from .models import DriverProfile, Trip, LogSheet
from .serializers import DriverProfileSerializer, TripSerializer, LogSheetSerializer, UserSerializer
import requests
from datetime import datetime, timedelta
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    
    user = User.objects.create_user(username=username, email=email, password=password)
    profile = DriverProfile.objects.create(user=user, name=name)
    
    return Response({
        'user': UserSerializer(user).data,
        'profile': DriverProfileSerializer(profile).data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user:
        login(request, user)
        profile = DriverProfile.objects.get(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'profile': DriverProfileSerializer(profile).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [AllowAny]  # Temporary for testing
    queryset = Trip.objects.all()

    def create(self, request):
        data = request.data
        print("Received data:", data)  # Debug log on backend
       
        trip = Trip.objects.create(
            user=None,  # No auth for now
            current_location=data['current_location'],
            pickup_location=data['pickup_location'],
            dropoff_location=data['dropoff_location'],
            current_cycle_used=float(data['current_cycle_used']),
            current_lat=data.get('current_lat'),
            current_lng=data.get('current_lng'),
            pickup_lat=data.get('pickup_lat'),
            pickup_lng=data.get('pickup_lng'),
            dropoff_lat=data.get('dropoff_lat'),
            dropoff_lng=data.get('dropoff_lng'),
            transport_type=data.get('transport_type', 'truck'),
        )
        
        # Optional: Generate mock logs (can be expanded later)
        logs = [
            LogSheet.objects.create(
                trip=trip, date=datetime.now().date(), duty_status='D',
                start_time=datetime.now().time(), end_time=(datetime.now() + timedelta(hours=1)).time(),
                location=trip.current_location
            )
        ]
        
        return Response({
            'trip': TripSerializer(trip).data,
            'route': {},  # Empty for now; add route calculation if needed
            'logs': LogSheetSerializer(logs, many=True).data
        }, status=status.HTTP_201_CREATED)
    
    def get_route_info(self, start, pickup, dropoff):
        # Using OpenRouteService as free map API (requires API key)
        api_key = 'YOUR_API_KEY'
        url = 'https://api.openrouteservice.org/v2/directions/driving-car'
        coords = f"{start}|{pickup}|{dropoff}"
        
        response = requests.get(
            url,
            params={
                'api_key': api_key,
                'coordinates': coords
            }
        )
        return response.json() if response.status_code == 200 else {}

    def generate_log_sheets(self, trip, route_info):
        logs = []
        current_time = datetime.now()
        remaining_hours = 70 - trip.current_cycle_used
        
        # Simplified log generation
        # Driving to pickup (assuming 1 hour for pickup)
        logs.append(LogSheet.objects.create(
            trip=trip,
            date=current_time.date(),
            duty_status='D',
            start_time=current_time.time(),
            end_time=(current_time + timedelta(hours=1)).time(),
            location=trip.current_location
        ))
        
        # Pickup time
        logs.append(LogSheet.objects.create(
            trip=trip,
            date=current_time.date(),
            duty_status='ON',
            start_time=(current_time + timedelta(hours=1)).time(),
            end_time=(current_time + timedelta(hours=2)).time(),
            location=trip.pickup_location
        ))
        
        return logs
