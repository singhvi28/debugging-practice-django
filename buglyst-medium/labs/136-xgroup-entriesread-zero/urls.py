from django.urls import path

from views import build_args

urlpatterns = [
    path("xgroup/args", build_args),
]
