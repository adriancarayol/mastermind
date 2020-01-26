"""
Module that contains the models for the games
"""
import uuid
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    """
    Class to represent the game model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    code_breaker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    attempts = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code_maker} vs {self.code_breaker}"
