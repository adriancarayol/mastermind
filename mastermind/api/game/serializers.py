"""
Module that contains the serializers for Game model
"""
from rest_framework import serializers
from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for Game model
    """

    class Meta:
        model = Game
        fields = ("code_maker", "code_breaker", "attempts", "id", "created_at")
        read_only_fields = ("code_maker", "created_at")
