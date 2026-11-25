from django.urls import path

from views import post_artifact

urlpatterns = [
    path("artifacts", post_artifact),
]
