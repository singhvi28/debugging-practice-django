from django.urls import path

from views import migrate, schema

urlpatterns = [
    path("migrate", migrate),
    path("schema", schema),
]
