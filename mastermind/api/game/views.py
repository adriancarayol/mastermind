"""
Module which contains views for users
"""
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from game.models import Game
from api.game.serializers import GameSerializer


class GameView(APIView):
    """
    List all users or create a new one.
    """
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logger.info(f'Request: {request} - format: {format}')
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(code_maker=request.user)
            logger.info(f'Game = {serializer.data} has been created.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.info(f'Bad request with errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        logger.info(f'Request: {request} - format: {format}')
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
