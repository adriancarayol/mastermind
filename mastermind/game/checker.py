"""
Module which contains utils to check the status of a game
"""
from enum import Enum
from code_peg.models import CodePeg
from game.models import Game


class CodeKey(Enum):
    """
    Class to represent the possibles values of the feedback
    """

    BLACK = "Black"
    WHITE = "White"
    BLANK = "Blank"


class GameChecker:
    """
    Class to control the status of a game
    """

    @staticmethod
    def is_solution(code_peg: CodePeg, game: Game) -> bool:
        """
        Given the code peg submitted and the current game,
        check if is a correct solution
        :param code_peg: CodePeg submitted
        :param game: Current game
        :return: True if the solution is valid, else False
        """

        try:
            solution = CodePeg.objects.get(game=game, is_solution=True)
        except CodePeg.DoesNotExist:
            return False

        solution_slots = (
            solution.slot1,
            solution.slot2,
            solution.slot3,
            solution.slot4,
        )
        submitted_slots = (
            code_peg.slot1,
            solution.slot2,
            solution.slot3,
            solution.slot4,
        )

        if solution_slots == submitted_slots:
            return True

        return False

    @staticmethod
    def is_the_game_finished(game: Game):
        """
        Given a Game, return True if the game is finished
        (code_breaker found the solution) or the code pegs submitted
        are equal or greater than the game attempts allowed.
        :param game: Game to check if is finished.
        :return: True if the game is finished, False in other case.
        """
        try:
            solution = CodePeg.objects.get(game=game, is_solution=True)
        except CodePeg.DoesNotExist:
            return False

        total_code_pegs = CodePeg.objects.filter(game=game, is_solution=False).count()
        solution_slots = (
            solution.slot1,
            solution.slot2,
            solution.slot3,
            solution.slot4,
        )

        for code_peg in CodePeg.objects.filter(game=game, is_solution=False):
            submitted_peg = (
                code_peg.slot1,
                code_peg.slot2,
                code_peg.slot3,
                code_peg.slot4,
            )
            if submitted_peg == solution_slots:
                return True

        if total_code_pegs >= game.attempts:
            return True

        return False

    @staticmethod
    def feedback_to_solution_provided(code_peg: CodePeg, game: Game) -> list:
        """
        Return a feedback for the solution provided
        :param code_peg: CodePeg provided
        :param game: Current game
        :return:
        """
        try:
            solution = CodePeg.objects.get(game=game, is_solution=True)
        except CodePeg.DoesNotExist:
            return []

        solution_slots = (
            solution.slot1,
            solution.slot2,
            solution.slot3,
            solution.slot4,
        )
        submitted_slots = (
            code_peg.slot1,
            code_peg.slot2,
            code_peg.slot3,
            code_peg.slot4,
        )

        feedback = [CodeKey.BLANK.value for _ in range(4)]

        # Fill black code keys
        for i, submitted in enumerate(submitted_slots):
            for j, solution in enumerate(solution_slots):
                if i == j and submitted == solution:
                    feedback[i] = CodeKey.BLACK.value

        # Fill white code keys
        for i, submitted in enumerate(submitted_slots):
            for j, solution in enumerate(solution_slots):
                if submitted == solution and feedback[i] != CodeKey.BLACK.value:
                    feedback[i] = CodeKey.WHITE.value

        return feedback
