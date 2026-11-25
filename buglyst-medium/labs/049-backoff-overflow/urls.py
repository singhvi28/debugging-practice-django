from django.urls import path

from views import get_backoff

urlpatterns = [
    path("backoff/<int:attempt>", get_backoff),
]
