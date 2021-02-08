from rest_framework import serializers
from .models import Driver, Location

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('__all__')
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude')