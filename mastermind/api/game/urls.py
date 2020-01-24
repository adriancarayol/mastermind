from django.urls import path
from api.game.views import GameView

app_name = 'game'

urlpatterns = [
    path('', GameView.as_view()),
]
