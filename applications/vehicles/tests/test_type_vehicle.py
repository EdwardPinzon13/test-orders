from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import  status
from django.contrib.auth.models import User
from applications.vehicles.routers import router

class TypeVehicleAPIViewTests(APITestCase):

    type_vehicle_url = reverse('type_vehicle-list')
    type_vehicle_urls_detail = reverse('type_vehicle-detail', args=[1])
    data_type_vehicle = {
                    'type_vehicle' : 'automovil'
                 }

    def setUp(self):
        self.user = User.objects.create_user(username='admin',password='admin@gmail.com')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response_detail = self.client.post(self.type_vehicle_url,data=self.data_type_vehicle, format='json')

    def tearDown(self):
        pass

    def test_get_type_vehicle_authenticated(self):
        response = self.client.get(self.type_vehicle_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_type_vehicle_authenticated(self):
        response = self.client.post(self.type_vehicle_url,data=self.data_type_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type_vehicle'],'automovil')

    def test_detail_type_vehicle_authenticated(self):
        response = self.client.get(self.type_vehicle_urls_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['type_vehicle'],'automovil')

    ### NOT AUTHENTICATE

    def test_get_type_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.type_vehicle_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_type_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.post(self.type_vehicle_url,data=self.data_type_vehicle, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_detail_type_vehicle_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.type_vehicle_urls_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


