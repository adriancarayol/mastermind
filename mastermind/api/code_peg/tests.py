import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from code_peg.models import CodePeg
from game.checker import CodeKey
from game.models import Game


@pytest.mark.django_db
class TestCodePegView:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        self.client = APIClient()
        u1 = User.objects.create(
            username="foo1", email="foo1@foo.com", password="foo123"
        )
        u2 = User.objects.create(
            username="foo2", email="foo2@foo.com", password="foo123"
        )
        game = Game.objects.create(code_maker=u1, code_breaker=u2, attempts=5)
        CodePeg.objects.create(
            game=game,
            is_solution=True,
            slot1=CodePeg.get_color_index(CodePeg.PURPLE),
            slot2=CodePeg.get_color_index(CodePeg.PURPLE),
            slot3=CodePeg.get_color_index(CodePeg.PURPLE),
            slot4=CodePeg.get_color_index(CodePeg.PURPLE),
        )

    def test_create_code_peg(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_breaker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": Game.objects.get().id,
            "slot1": CodePeg.get_color_index(CodePeg.ORANGE),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }

        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == [
            CodeKey.BLANK.value,
            CodeKey.BLACK.value,
            CodeKey.BLACK.value,
            CodeKey.BLACK.value,
        ]

    def test_create_code_peg_win_game(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_breaker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": Game.objects.get().id,
            "slot1": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }

        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_200_OK
        assert response.data == "You've won the game!"

    def test_create_code_peg_game_finished_with_winner(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_breaker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": Game.objects.get().id,
            "slot1": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }

        self.client.post(url, data, format="json")
        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_code_peg_game_finished_with_attemps(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_breaker)
        game = Game.objects.get()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": game.id,
            "slot1": CodePeg.get_color_index(CodePeg.RED),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }
        attempts = 5
        for code_peg in range(attempts):
            self.client.post(url, data, format="json")

        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data == f"The game: {game} is already over."

    def test_create_code_peg_with_duplicate_solution(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_maker = User.objects.get(username="foo1")
        token = Token.objects.create(user=code_maker)
        game = Game.objects.get()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": game.id,
            "slot1": CodePeg.get_color_index(CodePeg.RED),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }
        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_409_CONFLICT
        assert (
            response.data == f"One solution was provided before for this game: {game}"
        )

    def test_create_code_peg_unauthorized_game(self):
        url = reverse("api:code-pegs:code-pegs-view")
        u3 = User.objects.create(username="foo3", password="foo123")
        token = Token.objects.create(user=u3)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": Game.objects.get().id,
            "slot1": CodePeg.get_color_index(CodePeg.RED),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }
        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == "You can't play this game."

    def test_create_code_peg_bad_request(self):
        url = reverse("api:code-pegs:code-pegs-view")
        code_breaker = User.objects.get(username="foo2")
        token = Token.objects.create(user=code_breaker)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "slot1": CodePeg.get_color_index(CodePeg.ORANGE),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }

        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_code_peg_game_doesnt_started_yet(self):
        url = reverse("api:code-pegs:code-pegs-view")
        u1 = User.objects.create(username="foo3", password="foo123")
        u2 = User.objects.create(username="foo4", password="foo123")
        game = Game.objects.create(code_maker=u1, code_breaker=u2, attempts=1)
        token = Token.objects.create(user=u2)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        data = {
            "game": game.id,
            "slot1": CodePeg.get_color_index(CodePeg.ORANGE),
            "slot2": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot3": CodePeg.get_color_index(CodePeg.PURPLE),
            "slot4": CodePeg.get_color_index(CodePeg.PURPLE),
        }

        response = self.client.post(url, data, format="json")
        assert response
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.data == "The game isn't started yet."
