from django.urls import path

from views import last_echo, proxy_forward

urlpatterns = [
    path("forward", proxy_forward),
    path("internal/echo/last", last_echo),
]
