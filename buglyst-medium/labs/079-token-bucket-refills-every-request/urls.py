from django.urls import path

from views import admin_reset, get_resource

urlpatterns = [
    path("api/resource", get_resource),
    path("admin/reset", admin_reset),
]
