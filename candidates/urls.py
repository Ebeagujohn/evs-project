from django.urls import path
from . import views

app_name = "candidates"

urlpatterns = [
    path("add/", views.candidates_add, name="candidates_add"),
    path("access-denied/", views.candidates_access_denied, name="candidates_access_denied"),
]