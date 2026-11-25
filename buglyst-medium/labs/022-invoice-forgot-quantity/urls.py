from django.urls import path

from views import create_invoice

urlpatterns = [
    path("invoice", create_invoice),
]
