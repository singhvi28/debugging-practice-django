from django.urls import path

from views import bucket

urlpatterns = [
    path("events/bucket", bucket),
]
