from django.urls import path

from views import admin_reset, search

urlpatterns = [
    path("search", search),
    path("admin/reset", admin_reset),
]
