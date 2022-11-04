from django.urls import path

app_name = 'orders_app'
from .views import *

urlpatterns = [
    path('add-order/', AddOrder.as_view(), name='order_driver'),
    path('add-order-dynamic/', AddOrderWithDynamicDriver.as_view(), name='order_dynamic'),
    path('filter-order/', filterOrders.as_view(), name='filter_order'),
    #path('filter-order/<date>/', filterOrders.as_view(), name='filter_order'),
    path('driver-certain/', DriverCertain.as_view(), name='driver_certain'),


]
