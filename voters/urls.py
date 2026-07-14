from django.urls import path
from . import views

app_name = "voters"

urlpatterns = [
    path("register/", views.voters_register, name="voters_register"),
]
