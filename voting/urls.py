from django.urls import path
from . import views

app_name = "voting"

urlpatterns = [
    path("login/", views.voting_login, name="voting_login"),
    path("vote/", views.voting_cast_vote, name="voting_cast_vote"),
    path("results/", views.voting_results, name="voting_results"),
]
