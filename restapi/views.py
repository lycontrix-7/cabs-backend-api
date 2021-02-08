# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import DriverSerializer, LocationSerializer
from .models import Driver, Location
import math
import decimal
import json

def index(self):
    return HttpResponse("Hello, world. You're at Rest.")

class register(APIView):
    def post(self, request, format=None):
        
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.data.get('name')
            email = serializer.data.get('email')
            phone_number = serializer.data.get('phone_number')
            license_number = serializer.data.get('license_number')
            car_number = serializer.data.get('car_number')

            queryset = Driver.objects.filter(name=name)
            if not queryset.exists():
                driver = Driver(name=name, email=email, phone_number=phone_number, license_number=license_number, car_number=car_number)
                driver.save()
                return Response(DriverSerializer(driver).data, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "reason": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        
class location(APIView):
    def post(self, request, format=None, **kwargs):
        
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            
            latitude = serializer.data.get('latitude')
            longitude = serializer.data.get('longitude')
            driver = Driver.objects.get(id=self.kwargs['id'])
            
            location = Location(driver=driver, latitude=latitude, longitude=longitude)
            location.save()
            return Response({"status": "success"}, status=status.HTTP_202_ACCEPTED)
        return Response({"status": "failure", "reason": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        
class available(APIView):
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            
            latitude = serializer.data.get('latitude')
            longitude = serializer.data.get('longitude')
            
            all_locations = Location.objects.all()
            
            def hav(x):
                y = math.sin(x/2)
                return y*y
            
            def haversine(x1, y1, x2, y2):
                return 2*6371*math.asin(math.sqrt(hav(x1-x2) + math.cos(x1)*math.cos(x2)*hav(y1-y2)))
                
            available_cabs = []
            
            for loc in all_locations:
                d = haversine(loc.latitude, loc.longitude, decimal.Decimal(latitude), decimal.Decimal(longitude))
                if int(d) <= 4:
                    available_cabs.append(loc)
            
            cab_details = []
            
            for cabs in available_cabs:
                cab_details.append(
                    {
                        "name": f"{cabs.driver.name}",
                        "car_number": f"{cabs.driver.car_number}",
                        "phone_number": f"{cabs.driver.phone_number}"
                        }
                )
                
            if cab_details:
                return Response({"available_cabs": cab_details}, status=status.HTTP_200_OK)
            return Response({"message": "No cabs available!"}, status=status.HTTP_200_OK)
        return Response({"status": "failure", "reason": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)