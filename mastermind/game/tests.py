import pytest

from django.contrib.auth.models import User
from django.db import IntegrityError

from code_peg.models import CodePeg
from game.checker import GameChecker, CodeKey
from game.models import Game


@pytest.mark.django_db
class TestGameModel:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        User.objects.create(username="foo1", email="foo1@foo.com", password="foo123")
        User.objects.create(username="foo2", email="foo2@foo.com", password="foo123")

    def test_create_game(self):
        user_1 = User.objects.get(username="foo1")
        user_2 = User.objects.get(username="foo2")
        attempts = 6
        game = Game.objects.create(
            code_maker=user_1, code_breaker=user_2, attempts=attempts
        )

        assert game
        assert game.attempts == attempts
        assert game.code_maker == user_1
        assert game.code_breaker == user_2

    def test_create_game_invalid_code_maker(self):
        user_1 = User.objects.get(username="foo1")
        with pytest.raises(IntegrityError):
            Game.objects.create(code_maker=None, code_breaker=user_1)

    def test_create_game_invalid_code_breaker(self):
        user_1 = User.objects.get(username="foo1")

        with pytest.raises(IntegrityError):
            Game.objects.create(code_maker=user_1, code_breaker=None)

    def test_create_game_invalid_attempts(self):
        user_1 = User.objects.get(username="foo1")
        user_2 = User.objects.get(username="foo2")
        attempts = -1

        with pytest.raises(IntegrityError):
            Game.objects.create(
                code_maker=user_1, code_breaker=user_2, attempts=attempts
            )

    def test_list_all_games(self):
        user_1 = User.objects.get(username="foo1")
        user_2 = User.objects.get(username="foo2")
        attempts = 1
        g1 = Game.objects.create(
            code_maker=user_1, code_breaker=user_2, attempts=attempts
        )
        g2 = Game.objects.create(
            code_maker=user_2, code_breaker=user_1, attempts=attempts
        )
        games = Game.objects.all()

        assert games.count() == 2
        assert sorted([g1.id, g2.id]) == sorted([game.id for game in games])


@pytest.mark.django_db
class TestGameChecker:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        user1 = User.objects.create(
            username="foo1", email="foo1@foo.com", password="foo123"
        )
        user2 = User.objects.create(
            username="foo2", email="foo2@foo.com", password="foo123"
        )
        game = Game.objects.create(code_breaker=user1, code_maker=user2, attempts=4)
        CodePeg.objects.create(
            game=game,
            is_solution=True,
            slot1=CodePeg.get_color_index(CodePeg.BLUE),
            slot2=CodePeg.get_color_index(CodePeg.RED),
            slot3=CodePeg.get_color_index(CodePeg.ORANGE),
            slot4=CodePeg.get_color_index(CodePeg.GREEN),
        )

    @pytest.mark.parametrize(
        "slots, expected",
        [
            (
                (
                    CodePeg.get_color_index(CodePeg.BLUE),
                    CodePeg.get_color_index(CodePeg.RED),
                    CodePeg.get_color_index(CodePeg.ORANGE),
                    CodePeg.get_color_index(CodePeg.GREEN),
                ),
                True,
            ),
            (
                (
                    CodePeg.get_color_index(CodePeg.RED),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                ),
                False,
            ),
        ],
    )
    def test_is_solution(self, slots, expected):
        game = Game.objects.get()
        code_peg = CodePeg.objects.create(
            game=game, slot1=slots[0], slot2=slots[1], slot3=slots[2], slot4=slots[3]
        )
        is_solution = GameChecker.is_solution(code_peg, game)
        assert is_solution == expected

    @pytest.mark.parametrize("attempts, is_finished", [(3, False), (7, True)])
    def test_is_the_game_finished(self, attempts, is_finished):
        game = Game.objects.get()

        for _ in range(attempts):
            CodePeg.objects.create(game=game, slot1=1, slot2=1, slot3=1, slot4=1)

        assert GameChecker.is_the_game_finished(game) == is_finished

    @pytest.mark.parametrize(
        "slots, expected",
        [
            (
                (
                    CodePeg.get_color_index(CodePeg.ORANGE),
                    CodePeg.get_color_index(CodePeg.GREEN),
                    CodePeg.get_color_index(CodePeg.ORANGE),
                    CodePeg.get_color_index(CodePeg.BLUE),
                ),
                [
                    CodeKey.WHITE.value,
                    CodeKey.WHITE.value,
                    CodeKey.BLACK.value,
                    CodeKey.WHITE.value,
                ],
            ),
            (
                (
                    CodePeg.get_color_index(CodePeg.RED),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                ),
                [
                    CodeKey.WHITE.value,
                    CodeKey.BLANK.value,
                    CodeKey.BLANK.value,
                    CodeKey.BLANK.value,
                ],
            ),
            (
                (
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                    CodePeg.get_color_index(CodePeg.PURPLE),
                ),
                [
                    CodeKey.BLANK.value,
                    CodeKey.BLANK.value,
                    CodeKey.BLANK.value,
                    CodeKey.BLANK.value,
                ],
            ),
        ],
    )
    def test_feedback_to_solution_provided(self, slots, expected):
        game = Game.objects.get()
        code_peg = CodePeg.objects.create(
            game=game, slot1=slots[0], slot2=slots[1], slot3=slots[2], slot4=slots[3]
        )

        feedback = GameChecker.feedback_to_solution_provided(code_peg, game)
        assert feedback == expected
