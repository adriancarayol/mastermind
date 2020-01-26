import pytest
from django.db import IntegrityError
from django.contrib.auth.models import User

from code_peg.models import CodePeg
from game.models import Game


@pytest.mark.django_db
class TestCodePeg:
    @pytest.fixture(autouse=True)
    def setup_games(self):
        code_maker = User.objects.create(username="foo1", password="foo123")
        code_breaker = User.objects.create(username="foo2", password="foo123")
        Game.objects.create(
            code_maker=code_maker, code_breaker=code_breaker, attempts=6
        )

    @pytest.mark.parametrize(
        "color, expected",
        [
            (CodePeg.YELLOW, 1),
            (CodePeg.BLUE, 2),
            (CodePeg.PURPLE, 3),
            (CodePeg.ORANGE, 4),
            (CodePeg.GREEN, 5),
            (CodePeg.RED, 6),
            ("Black", -1),
        ],
    )
    def test_get_color_index(self, color, expected):
        index = CodePeg.get_color_index(color)
        assert index == expected

    def test_create_code_peg(self):
        game = Game.objects.get()
        code_peg = CodePeg.objects.create(
            game=game,
            slot1=CodePeg.get_color_index(CodePeg.YELLOW),
            slot2=CodePeg.get_color_index(CodePeg.YELLOW),
            slot3=CodePeg.get_color_index(CodePeg.RED),
            slot4=CodePeg.get_color_index(CodePeg.BLUE),
        )
        assert code_peg
        assert not code_peg.is_solution
        assert code_peg.slot1 == CodePeg.get_color_index(CodePeg.YELLOW)
        assert code_peg.slot2 == CodePeg.get_color_index(CodePeg.YELLOW)
        assert code_peg.slot3 == CodePeg.get_color_index(CodePeg.RED)
        assert code_peg.slot4 == CodePeg.get_color_index(CodePeg.BLUE)
        assert code_peg.game == game

    def test_create_code_peg_without_game(self):
        with pytest.raises(IntegrityError):
            CodePeg.objects.create(slot1=1, slot2=6, slot3=5, slot4=2)
