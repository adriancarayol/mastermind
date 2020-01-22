"""
Module that contains the serializers for User model
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Seriaizer for User model
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'id')
