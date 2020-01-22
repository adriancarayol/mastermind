import pytest

from django.contrib.auth.models import User
from django.db import IntegrityError

from game.models import Game


@pytest.mark.django_db
class TestGameModel:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        User.objects.create(username="foo1", email="foo1@foo.com", password="foo123")
        User.objects.create(username="foo2", email="foo2@foo.com", password="foo123")

    def test_create_game(self):
        user_1 = User.objects.get(username='foo1')
        user_2 = User.objects.get(username='foo2')
        attempts = 1
        game = Game.objects.create(code_maker=user_1, code_breaker=user_2, attempts=attempts)

        assert game
        assert game.attempts == attempts
        assert game.code_maker == user_1
        assert game.code_breaker == user_2

    def test_create_game_invalid_code_maker(self):
        user_1 = User.objects.get(username='foo1')
        with pytest.raises(IntegrityError):
            Game.objects.create(code_maker=None, code_breaker=user_1)

    def test_create_game_invalid_code_breaker(self):
        user_1 = User.objects.get(username='foo1')

        with pytest.raises(IntegrityError):
            Game.objects.create(code_maker=user_1, code_breaker=None)

    def test_create_game_invalid_attempts(self):
        user_1 = User.objects.get(username='foo1')
        user_2 = User.objects.get(username='foo2')
        attempts = -1

        with pytest.raises(IntegrityError):
            Game.objects.create(code_maker=user_1, code_breaker=user_2, attempts=attempts)

    def test_list_all_games(self):
        user_1 = User.objects.get(username='foo1')
        user_2 = User.objects.get(username='foo2')
        attempts = 1
        g1 = Game.objects.create(code_maker=user_1, code_breaker=user_2, attempts=attempts)
        g2 = Game.objects.create(code_maker=user_2, code_breaker=user_1, attempts=attempts)
        games = Game.objects.all()

        assert games.count() == 2
        assert sorted([g1.id, g2.id]) == sorted([game.id for game in games])
