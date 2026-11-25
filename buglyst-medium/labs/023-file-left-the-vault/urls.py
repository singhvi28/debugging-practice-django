from django.urls import path

from views import get_file

urlpatterns = [
    path("files", get_file),
]
