from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import  status
from django.contrib.auth.models import User
from applications.vehicles.routers import router
from .test_type_vehicle import TypeVehicleAPIViewTests 
from .test_brand_api import BrandAPIViewTests
from applications.vehicles.models import *
class VehicleAPIViewTests(APITestCase):

    type_vehicle_url = reverse('type_vehicle-list')
    brand_url = reverse('brand-list')
    vehicle_url = reverse('vehicle-list')
    vehicle_urls_detail = reverse('vehicle-detail', args=[1])



    type_vehicle = TypeVehicleAPIViewTests.data_type_vehicle
    brand =  BrandAPIViewTests.data_brand



    def setUp(self):
        self.user = User.objects.create_user(username='admin',password='admin@gmail.com')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        self.response_type_vehicle = self.client.post(self.type_vehicle_url,data=self.type_vehicle, format='json')
        self.response_brand = self.client.post(self.brand_url,data=self.brand, format='json')
        brand_object = Brand.objects.get(id=self.response_brand.data['id']).id
        type_vehicle_object = TypeVehicle.objects.get(id=self.response_type_vehicle.data['id']).id

        self.vehicle_data = {
            'modelo' : 2018,
            'brand' : self.response_brand.data['id'],
            'type_vehicle' : self.response_type_vehicle.data['id'],
            'plate' : 'ddrx2'
        }
        response_vehicle = self.client.post(self.vehicle_url,self.vehicle_data,format='json')

    def tearDown(self):
        pass

    def test_get_vehicle_authenticated(self):
        response = self.client.get(self.vehicle_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_vehicle_authenticated(self):
        response = self.client.post(self.vehicle_url,self.vehicle_data,format='json')
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['modelo'], 2018)
        return response

        #self.assertEqual(response.data['type_vehicle'],'automovil')

    def test_detail_vehicle_authenticated(self):
        response = self.client.get(self.vehicle_urls_detail)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['modelo'],2018)

    ### NOT AUTHENTICATE

    def test_get_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.vehicle_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.post(self.vehicle_url,data=self.vehicle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_detail_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.vehicle_urls_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


