from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class TypeVehicleViewSet(viewsets.ModelViewSet):
    queryset = TypeVehicle.objects.all()
    serializer_class = TypeVehicleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]