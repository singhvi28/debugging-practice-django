from django.urls import path

from views import admin_reset, api_data

urlpatterns = [
    path("api/data", api_data),
    path("admin/reset", admin_reset),
]
