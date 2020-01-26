"""
Module which contains views for games
"""
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.code_peg.serializers import CodePegSerializer
from code_peg.models import CodePeg
from game.models import Game
from api.game.serializers import GameSerializer


class GameView(APIView):
    """
    List all users or create a new one.
    """

    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Method to handle POST requests.
        Creates a new game
        """
        logger.info(f"Request: {request}. args: {args}, kwargs: {kwargs}")
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            code_breaker = serializer.validated_data["code_breaker"]

            if code_breaker == request.user.id:
                return Response(
                    f"You cannot play with yourself!",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(code_maker=request.user)
            logger.info(f"Game = {serializer.data} has been created.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.info(f"Bad request with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        Method to handle GET requests.
        Returns all the games in DB.
        """
        logger.info(f"Request: {request}. args: {args}, kwargs: {kwargs}")
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


class GameHistoricView(APIView):
    """
    View class to handle the game historic
    """
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logger.info(f"Request: {request}. args: {args}, kwargs: {kwargs}")
        game_id = kwargs.get('id')
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        code_pegs = CodePeg.objects.filter(game=game, is_solution=False)
        serializer = CodePegSerializer(code_pegs, many=True)
        return Response(serializer.data)
