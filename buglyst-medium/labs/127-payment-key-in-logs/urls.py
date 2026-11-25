from django.urls import path

from views import post_charge

urlpatterns = [
    path("charge", post_charge),
]
