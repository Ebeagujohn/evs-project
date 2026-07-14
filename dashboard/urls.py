from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("voters/", views.dashboard_voters_list, name="dashboard_voters_list"),
]