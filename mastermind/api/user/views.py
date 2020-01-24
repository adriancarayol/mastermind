"""
Module which contains views for users
"""
from django.contrib.auth.models import User
from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from api.user.serializers import UserSerializer


class UserView(APIView):
    """
    List all users or create a new one.
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        logger.info(f'Request: {request} - format: {format}')
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            username = serializer.data.get('username')
            logger.info(f'User with username: {username} has been created.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.info(f'Bad request with errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        logger.info(f'Request: {request} - format: {format}')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
