from django.urls import path

from views import resolve_secret

urlpatterns = [
    path("deploy/secret", resolve_secret),
]
