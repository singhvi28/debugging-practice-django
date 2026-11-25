from django.urls import path

from views import read_config

urlpatterns = [
    path("config", read_config),
]
