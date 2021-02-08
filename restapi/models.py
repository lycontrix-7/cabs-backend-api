# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator  

class Driver(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.IntegerField(unique=True, validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    license_number = models.CharField(max_length=100, unique=True)
    car_number = models.CharField(max_length=100, unique=True)
    
    # def __str__(self):
    #     return self.id
    
class Location(models.Model):
    driver = models.OneToOneField(Driver ,on_delete=models.CASCADE, primary_key=True)
    latitude = models.DecimalField(max_digits=20,decimal_places=10, unique=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, unique=False)

  