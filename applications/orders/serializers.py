from rest_framework import serializers
from .models import *

from applications.driver.serializers import DriverSerializer

class OrderSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class AddOrderSerializer(serializers.Serializer):
    driver = serializers.IntegerField(required=True, help_text="ID of driver to Asign")
    date = serializers.DateField(required=True)
    hour = serializers.TimeField(required=True, help_text="Hour Format %H:%M:%S")
    pickup_place = serializers.JSONField(required=True, help_text='Pickup_place Format {"lat": "valor-lat , "lng" : "valor-lng"}')
    destination_place = serializers.JSONField(required=True,help_text='destination_place Format {"lat": "valor-lat , "lng" : "valor-lng"}')

class AddOrderDynamicSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    hour = serializers.TimeField(required=True, help_text="Hour Format %H:%M:%S")
    pickup_place = serializers.JSONField(required=True, help_text='Pickup_place Format {"lat": "valor-lat , "lng" : "valor-lng"}')
    destination_place = serializers.JSONField(required=True,help_text='destination_place Format {"lat": "valor-lat , "lng" : "valor-lng"}')

class FindTheNearestDriverSerializer(serializers.Serializer):
    location = serializers.JSONField(required=True, help_text='location Format {"lat": "valor-lat , "lng" : "valor-lng"}')
    date = serializers.DateField(required=True)
    hour = serializers.TimeField(required=True, help_text="Hour Format %H:%M:%S")

class SearchOrdersSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    driver = serializers.IntegerField(required=False, help_text="ID of driver to Search")

