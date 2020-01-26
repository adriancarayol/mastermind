import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


@pytest.mark.django_db
class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse("api:users:users-view")
        data = {"username": "foo", "password": "foo123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "foo")

    def test_create_user_already_exists(self):
        url = reverse("api:users:users-view")
        data = {"username": "i_am_a_exiting_user", "password": "foo123"}
        self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "i_am_a_exiting_user")

    def test_create_invalid_username(self):
        url = reverse("api:users:users-view")
        data = {"username": "", "password": "foo123", "email": "email@es.es"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data["username"]
        self.assertEqual(response_data[0], "This field may not be blank.")

    def test_create_without_username(self):
        url = reverse("api:users:users-view")
        data = {"password": "foo123", "email": "email@es.es"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data["username"]
        self.assertEqual(response_data[0], "This field is required.")

    def test_create_invalid_password(self):
        url = reverse("api:users:users-view")
        data = {"username": "foo", "password": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data["password"]
        self.assertEqual(response_data[0], "This field may not be blank.")

    def test_create_without_password(self):
        url = reverse("api:users:users-view")
        data = {"username": "foo123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data["password"]
        self.assertEqual(response_data[0], "This field is required.")

    def test_list_users(self):
        url = reverse("api:users:users-view")
        data = {"username": "foo", "password": "foo123", "email": "email@es.es"}
        data2 = {"username": "foo2", "password": "foo123"}
        self.client.post(url, data, format="json")
        self.client.post(url, data2, format="json")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            sorted([user["username"] for user in response.data]),
            sorted(["foo", "foo2"]),
        )
