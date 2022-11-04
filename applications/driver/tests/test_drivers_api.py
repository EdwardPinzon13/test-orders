from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import  status
from django.contrib.auth.models import User
from applications.driver.models import *
from applications.vehicles.models import *

from applications.vehicles.tests.test_vehicle_api import  VehicleAPIViewTests
class DriversPIViewTests(APITestCase):

    vehicle_url = reverse('vehicle-list')
    driver_url = reverse('driver-list')
    driver_urls_detail = reverse('driver-detail', args=[1])


    def getDataDriverJSONConstructor(self):
        brand = Brand.objects.create(
            brand_name = 'ferrari'
        )
        type_vehicle = TypeVehicle.objects.create(
            type_vehicle = 'automovil de lujo'
        )
        vehicle = Vehicle.objects.create(
            modelo = 2018,
            brand = brand,
            type_vehicle = type_vehicle,
            plate = 'ddrx2'
        )
        data_driver = {
            'name' : 'Francisco',
            'last_name' : 'Barbosa',
            'nuip' : 1234788642,
            'vehicle' : vehicle.id
        }
        return data_driver

    driver = getDataDriverJSONConstructor
    def setUp(self):
        self.user = User.objects.create_user(username='admin',password='admin@gmail.com')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response_driver = self.client.post(self.driver_url,self.getDataDriverJSONConstructor(),format='json')

    def tearDown(self):
        pass

    def test_get_vehicle_authenticated(self):
        response = self.client.get(self.driver_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_vehicle_authenticated(self):
        response = self.client.post(self.driver_url,self.getDataDriverJSONConstructor(),format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #self.assertEqual(response.data['type_vehicle'],'automovil')

    def test_detail_vehicle_authenticated(self):
        response = self.client.get(self.driver_urls_detail)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    ### NOT AUTHENTICATE

    def test_get_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.driver_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.post(self.driver_url,data=self.getDataDriverJSONConstructor(), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_detail_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.driver_urls_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
