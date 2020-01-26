from django.urls import path
from api.user.views import UserView

app_name = "api_user"

urlpatterns = [
    path("", UserView.as_view(), name="users-view"),
]
