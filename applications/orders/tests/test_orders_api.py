from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from applications.driver.models import *
from applications.vehicles.models import *
from applications.orders.models import *
from applications.driver.tests.test_drivers_api import DriversPIViewTests


class OrdersAPIViewTests(APITestCase):

    url_add_order = reverse('orders_app:order_driver')
    url_filter_order = reverse('orders_app:filter_order')
    url_driver_certain = reverse('orders_app:driver_certain')

    def getDataDriverJSONConstructor(self):
        brand = Brand.objects.create(
            brand_name='ferrari'
        )
        type_vehicle = TypeVehicle.objects.create(
            type_vehicle='automovil de lujo'
        )
        vehicle = Vehicle.objects.create(
            modelo=2018,
            brand=brand,
            type_vehicle=type_vehicle,
            plate='ddrx2'
        )
        data_driver = {
            'name': 'Francisco',
            'last_name': 'Barbosa',
            'nuip': 1234788642,
            'vehicle': vehicle
        }

        driver = Driver.objects.create(**data_driver)

        return driver

    data_order_correct = {
                    "driver": 1,
                    "date": "2022-11-09",
                    "hour": "02:03:00",
                    "pickup_place":
                    {
                        "lat": 8,
                        "lng": 11
                    },
                    "destination_place":
                    {
                        "lat": 15,
                        "lng": 90
                    }
                }



    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='admin@gmail.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        self.data_order_correct['driver'] = self.getDataDriverJSONConstructor().id



    def test_AddOrder_Authenticated(self):
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],'Servicio reservado con exito')


    def test_AddOrder_Incorrect_Driver(self):
        self.data_order_correct['driver'] = 30
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_AddOrder_Incorrect_Format_Date(self):
        self.data_order_correct['date'] = "2022-11-"
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_AddOrder_Incorrect_Format_Hour(self):
        self.data_order_correct['hour'] = "02:03"
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_AddOrder_Incorrect_Pickup_Place(self):
        self.data_order_correct['pickup_place'] = {"lat" : 9}
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_AddOrder_Incorrect_Format_Destination_Place(self):
        self.data_order_correct['destination_place'] = {"lng" : 8}
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ###  filterOrders

    def create_order(self):
        data_order_correct = {
                    "driver": 1,
                    "date": "2022-11-09",
                    "hour": "02:03:00",
                    "pickup_place":
                    {
                        "lat": 8,
                        "lng": 11
                    },
                    "destination_place":
                    {
                        "lat": 1,
                        "lng": 5
                    }
                }

        response_order = self.client.post(self.url_add_order,data_order_correct, format = 'json')
        return response_order.data['body']['id']

    filters = {
            "date" : "2022-11-09",
            "driver" : 1
    }

    def test_filterOrders_Authenticated(self):
        self.filters['driver'] = self.create_order()
        response = self.client.get(self.url_filter_order,self.filters, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filterOrders_WithOut_Driver(self):
        self.create_order()
        self.filters.pop('driver')
        response = self.client.get(self.url_filter_order,self.filters, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filterOrders_Incorrect_Format_Date(self):
        self.create_order()
        response = self.client.get(self.url_filter_order,{"date" : "2022-999"}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


    def test_filterOrders_Not_Found(self):
        self.create_order()
        response = self.client.get(self.url_filter_order,{"date" : "2022-10-12"}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    ### DriverCertain
    def getJsonDataForDriverCertain(self):
        driver_certain = {
            "location" : {
                "lat" : 1 ,
                "lng" : 5
            },
            "date" : "2022-11-03",
            "hour" : "02:10:00"
        }
        return driver_certain


    def test_DriverCertain_Driver_Authenticated(self):
        order = self.create_order()
        driver_data = self.getJsonDataForDriverCertain()
        response = self.client.post(self.url_driver_certain, driver_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_DriverCertain_Driver_Not_Found(self):
        driver_data = self.getJsonDataForDriverCertain()
        driver_data['location'] = {"lat" : 10 ,"lng" : 50}
        response = self.client.post(self.url_driver_certain, driver_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_DriverCertain_Incorrect_Format_Date(self):
        driver_data = self.getJsonDataForDriverCertain()
        driver_data['date'] = "2022-90"
        response = self.client.post(self.url_driver_certain, driver_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_DriverCertain_Incorrect_Format_Hour(self):
        driver_data = self.getJsonDataForDriverCertain()
        driver_data['hour'] = "10:00"
        response = self.client.post(self.url_driver_certain, driver_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




    ### NOT AUTHENTICATE
    def test_AddOrder_un_Authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.post(self.url_add_order,self.data_order_correct, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filterOrders_un_Authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.url_filter_order,self.filters, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#import pdb; pdb.set_trace()
    def tearDown(self):
        pass