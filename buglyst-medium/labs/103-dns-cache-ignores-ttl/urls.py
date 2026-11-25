from django.urls import path

from views import resolve_host, rotate

urlpatterns = [
    path("resolve", resolve_host),
    path("rotate", rotate),
]
