from django.urls import reverse,resolve
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import  status
from django.contrib.auth.models import User
from applications.vehicles.routers import router

class BrandAPIViewTests(APITestCase):

    brand_url = reverse('brand-list')
    brand_urls_detail = reverse('brand-detail', args=[1])

    data_brand = {
                    'brand_name' : 'peugeot'
                 }

    def setUp(self):
        self.user = User.objects.create_user(username='admin',password='admin@gmail.com')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        response_detail = self.client.post(self.brand_url,data=self.data_brand, format='json')
    def tearDown(self):
        pass

    def test_get_brands_authenticated(self):
        response = self.client.get(self.brand_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_brands_authenticated(self):
        response = self.client.post(self.brand_url,data=self.data_brand, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['brand_name'],'peugeot')

    def test_detail_brands_authenticated(self):
        response = self.client.get(self.brand_urls_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['brand_name'],'peugeot')

    ### NOT AUTHENTICATE

    def test_get_brands_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.brand_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_brands_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.post(self.brand_url,data=self.data_brand, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_detail_brands_un_authenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response = self.client.get(self.brand_urls_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


