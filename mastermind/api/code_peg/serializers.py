"""
Module that contains the serializers for CodePeg model
"""
from rest_framework import serializers
from code_peg.models import CodePeg


class CodePegSerializer(serializers.ModelSerializer):
    """
    Serializer for Game model
    """

    slot1 = serializers.ChoiceField(choices=CodePeg.COLORS)

    class Meta:  # pylint: disable-msg=R0903
        """
        Meta info for serializer
        """

        model = CodePeg
        fields = ("game", "slot1", "slot2", "slot3", "slot4")
