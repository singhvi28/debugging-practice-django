from django.urls import path

from views import beta_endpoint, features

urlpatterns = [
    path("features", features),
    path("beta", beta_endpoint),
]
