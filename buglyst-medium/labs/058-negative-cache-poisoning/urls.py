from django.urls import path

from views import record_handler

urlpatterns = [
    path("records/<str:key>", record_handler),
]
