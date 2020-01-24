from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('users', include('api.user.urls', namespace='users')),
    path('games', include('api.game.urls', namespace='games')),
]
