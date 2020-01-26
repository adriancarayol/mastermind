import uuid
import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from game.models import Game


@pytest.mark.django_db
class GameTests(APITestCase):
    @pytest.fixture(autouse=True)
    def setup_users(self):
        self.client = APIClient()
        User.objects.get_or_create(
            username="foo1", email="foo1@foo.com", password="foo123"
        )
        User.objects.get_or_create(
            username="foo2", email="foo2@foo.com", password="foo123"
        )

    def test_create_game(self):
        url = reverse("api:games:games-view")
        code_maker = User.objects.get(username="foo1")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_maker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {"attempts": 5, "code_breaker": code_breaker.id}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code_maker"], code_maker.id)
        self.assertEqual(response.data["code_breaker"], code_breaker.id)
        self.assertEqual(response.data["attempts"], 5)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Game.objects.get().attempts, 5)

    def test_create_game_unauthorized(self):
        url = reverse("api:games:games-view")
        code_breaker = User.objects.get(username="foo2")
        data = {"attempts": 5, "code_breaker": code_breaker.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_game_without_code_breaker(self):
        url = reverse("api:games:games-view")
        code_maker = User.objects.get(username="foo1")

        token = Token.objects.create(user=code_maker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {"attempts": 5}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code_breaker"][0], "This field is required.")

    def test_create_game_user_doesnt_exists(self):
        url = reverse("api:games:games-view")
        code_maker = User.objects.get(username="foo1")

        token = Token.objects.create(user=code_maker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        user_ids = sum([user.id for user in User.objects.all()])

        data = {"attempts": 5, "code_breaker": user_ids}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class GameHistoricTests(APITestCase):
    @pytest.fixture(autouse=True)
    def setup_users(self):
        self.client = APIClient()
        User.objects.get_or_create(
            username="foo1", email="foo1@foo.com", password="foo123"
        )
        User.objects.get_or_create(
            username="foo2", email="foo2@foo.com", password="foo123"
        )

    def test_get_game_historic(self):
        code_maker = User.objects.get(username="foo1")
        code_breaker = User.objects.get(username="foo2")
        game = Game.objects.create(code_breaker=code_breaker, code_maker=code_maker, attempts=1)
        token = Token.objects.create(user=code_maker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        url = reverse("api:game:game-historic", kwargs={'id': game.id})
        response = self.client.get(url)

        assert response
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_game_historic_game_not_found(self):
        code_maker = User.objects.get(username="foo1")
        token = Token.objects.create(user=code_maker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        url = reverse("api:game:game-historic", kwargs={'id': str(uuid.uuid4())})
        response = self.client.get(url)

        assert response
        assert response.status_code == status.HTTP_404_NOT_FOUND
