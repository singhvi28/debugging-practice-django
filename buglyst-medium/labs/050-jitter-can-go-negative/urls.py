from django.urls import path

from views import compute_jitter

urlpatterns = [
    path("jitter", compute_jitter),
]
