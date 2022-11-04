from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()

router.register('brand', BrandViewSet,basename='brand')
router.register('type-vehiclee', TypeVehicleViewSet,basename='type_vehicle')
router.register('vehicle', VehicleViewSet,basename='vehicle')

urlpatterns = router.urls