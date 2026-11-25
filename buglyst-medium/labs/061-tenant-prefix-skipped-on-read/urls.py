from django.urls import path

from views import kv_endpoint

urlpatterns = [
    path("kv/<str:tenant>/<str:key>", kv_endpoint),
]
