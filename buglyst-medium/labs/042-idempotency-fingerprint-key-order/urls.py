from django.urls import path

from views import create_operation

urlpatterns = [
    path("operations", create_operation),
]
