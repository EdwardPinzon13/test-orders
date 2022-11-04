from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()

router.register('driver', DriverViewSet,basename='driver')


urlpatterns = router.urls