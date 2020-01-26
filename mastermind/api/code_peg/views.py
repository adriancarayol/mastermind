"""
Module which contains views for code pegs
"""
from loguru import logger
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


from code_peg.models import CodePeg
from game.checker import GameChecker
from game.models import Game
from api.code_peg.serializers import CodePegSerializer


class CodePegView(APIView):
    """
    List all code pegs or create a new one.
    """

    serializer_class = CodePegSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Function to handle post requests.
        Creates a new CodePeg
        """
        logger.info(f"Request: {request}. args: {args}, kwargs: {kwargs}")
        serializer = CodePegSerializer(data=request.data)

        if serializer.is_valid():
            game = serializer.validated_data["game"]
            user = request.user

            code_maker = game.code_maker

            if GameChecker.is_the_game_finished(game):
                return Response(
                    f"The game: {game} is already over.",
                    status=status.HTTP_409_CONFLICT,
                )

            # Request made by the game owner
            if code_maker == user:
                if CodePeg.objects.filter(game=game, is_solution=True).exists():
                    return Response(
                        f"One solution was provided before for this game: {game}",
                        status=status.HTTP_409_CONFLICT,
                    )
                serializer.save(is_solution=True)
            # Request made by the code breaker.
            elif game.code_breaker == user:
                if not CodePeg.objects.filter(game=game, is_solution=True).exists():
                    return Response(
                        "The game isn't started yet.", status=status.HTTP_409_CONFLICT
                    )

                code_peg = serializer.save()

                if GameChecker.is_solution(code_peg, game):
                    return Response(f"You've won the game!")

                feedback = GameChecker.feedback_to_solution_provided(code_peg, game)
                return Response(feedback, status=status.HTTP_201_CREATED)

            else:
                return Response(
                    "You can't play this game.", status=status.HTTP_403_FORBIDDEN
                )

        logger.info(f"Bad request with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Function to handle GET requests.
        Returns the code pegs where the code breaker is the
        request user
        """
        logger.info(f"Request: {request}. args: {args}, kwargs: {kwargs}")
        user = request.user

        try:
            game = Game.objects.get(code_breaker=user)
            code_pegs = CodePeg.objects.filter(game=game)
            serializer = CodePegSerializer(code_pegs, many=True)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response()
