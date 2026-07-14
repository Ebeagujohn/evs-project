from django.urls import path
from . import views

app_name = "candidates"

urlpatterns = [
    path("add/", views.candidates_add, name="candidates_add"),
]
