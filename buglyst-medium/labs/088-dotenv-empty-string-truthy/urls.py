from django.urls import path

from views import status, work

urlpatterns = [
    path("status", status),
    path("work", work),
]
