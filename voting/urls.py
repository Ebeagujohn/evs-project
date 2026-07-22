from django.urls import path
from . import views

app_name = "voting"

urlpatterns = [
    path("login/", views.voting_login, name="voting_login"),
    path("vote/", views.voting_cast_vote, name="voting_cast_vote"),
    path("thank-you/", views.voting_thank_you, name="voting_thank_you"),
    path("results/", views.voting_results, name="voting_results"),
    path("election-settings/", views.election_settings, name="voting_election_settings"),
    path("logout/", views.voting_logout, name="voting_logout"),
]