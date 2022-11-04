from rest_framework import serializers
from .models import *

from applications.vehicles.serializers import VehicleSerializer

class DriverSerializer(serializers.ModelSerializer):
    #vehicle = VehicleSerializer()
    class Meta:
        model = Driver
        fields = '__all__'