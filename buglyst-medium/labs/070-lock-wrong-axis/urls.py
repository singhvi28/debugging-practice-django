from django.urls import path

from views import reset, reserve

urlpatterns = [
    path("reserve", reserve),
    path("admin/reset", reset),
]
