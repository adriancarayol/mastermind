"""
Module which contains CodePeg models
"""

from django.db import models

from game.models import Game


class CodePeg(models.Model):
    """
    Class to represent a single code peg in a game
    """

    YELLOW = "Yellow"
    BLUE = "Blue"
    PURPLE = "Purple"
    ORANGE = "Orange"
    GREEN = "Green"
    RED = "Red"

    COLORS = (
        (1, YELLOW),
        (2, BLUE),
        (3, PURPLE),
        (4, ORANGE),
        (5, GREEN),
        (6, RED),
    )

    slot1 = models.IntegerField(choices=COLORS)
    slot2 = models.IntegerField(choices=COLORS)
    slot3 = models.IntegerField(choices=COLORS)
    slot4 = models.IntegerField(choices=COLORS)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="code_pegs")
    is_solution = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Position 1={self.slot1}, position 2: {self.slot2}, "
            f"position 3: {self.slot3}, position 4: {self.slot4}"
        )

    @staticmethod
    def get_color_index(color: str) -> int:
        """
        Return the color index given the color name
        :param color: Color name, for example, Yellow
        :return: Index value of the color. If the color not found, returns -1
        """
        color_index_position = 0
        color_name_position = 1

        for color_tuple in CodePeg.COLORS:
            if color_tuple[color_name_position] == color:
                return color_tuple[color_index_position]

        return -1
