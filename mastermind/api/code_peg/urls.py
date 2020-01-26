from django.urls import path
from api.code_peg.views import CodePegView

app_name = "code_peg"

urlpatterns = [
    path("", CodePegView.as_view(), name="code-pegs-view"),
]
