from django.urls import path

from views import debug_fetches, report

urlpatterns = [
    path("report", report),
    path("_debug/backend-fetches", debug_fetches),
]
