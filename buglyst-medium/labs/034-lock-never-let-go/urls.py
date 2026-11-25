from django.urls import path

from views import admin_reset, run_job

urlpatterns = [
    path("jobs", run_job),
    path("admin/reset", admin_reset),
]
