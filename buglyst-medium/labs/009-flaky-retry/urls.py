from django.urls import path

from views import debug_attempts, status

urlpatterns = [
    path("status", status),
    path("_debug/upstream-attempts", debug_attempts),
]
