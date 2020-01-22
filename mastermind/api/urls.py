from django.urls import path, re_path, include

urlpatterns = [
    path('', include('api.user.urls', namespace='user')),
]
