from django.urls import path

from views import decode

urlpatterns = [
    path("decode", decode),
]
