from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingridient

from recipe.serializers import IngridientSerializer


INGRIDIENTS_URL = reverse('recipe:ingridient-list')


class PublicIngridientsApiTests(TestCase):
    """Test the publicly available ingridient API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngridientsApiTests(TestCase):
    """Test the private ingridients api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingridients_list(self):
        """Test a retrieving a list of ingridients"""
        Ingridient.objects.create(user=self.user, name='Kale')
        Ingridient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGRIDIENTS_URL)

        ingridients = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(ingridients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingridients_limited_for_user(self):
        """Test that ingridients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'otherpass'
        )
        Ingridient.objects.create(user=user2, name='Vinegar')
        ingridient = Ingridient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingridient.name)

    def test_ingridient_successful(self):
        """Test create a new ingridient"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGRIDIENTS_URL, payload)

        exists = Ingridient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_ingridient_invalid(self):
        """Test creating invalid ingridient fails"""
        payload = {'name': ''}
        res = self.client.post(INGRIDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
