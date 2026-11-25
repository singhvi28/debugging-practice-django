from django.urls import path

from views import debug_processed, run_jobs

urlpatterns = [
    path("jobs/run", run_jobs),
    path("_debug/processed", debug_processed),
]
