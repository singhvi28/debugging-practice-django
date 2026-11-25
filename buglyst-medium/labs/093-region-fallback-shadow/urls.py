from django.urls import path

from views import deploy_region

urlpatterns = [
    path("deploy/region", deploy_region),
]
