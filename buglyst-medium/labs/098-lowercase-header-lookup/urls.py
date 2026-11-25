from django.urls import path

from views import protected

urlpatterns = [
    path("protected", protected),
]
