"""
Module that contains the serializers for Game model
"""
from game.models import Game
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for Game model
    """
    class Meta:
        model = Game
        fields = ('code_maker', 'code_breaker', 'attempts', 'id')
        read_only_fields = ('code_maker', )