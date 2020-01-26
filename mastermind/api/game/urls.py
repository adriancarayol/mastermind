from django.urls import path
from api.game.views import GameView, GameHistoricView

app_name = "game"

urlpatterns = [
    path("", GameView.as_view(), name="games-view"),
    path("/<str:id>/historic", GameHistoricView.as_view(), name="game-historic"),
]
