from django.urls import path

from views import rotate, submit

urlpatterns = [
    path("rotate", rotate),
    path("submit", submit),
]
