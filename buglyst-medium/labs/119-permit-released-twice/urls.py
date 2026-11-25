from django.urls import path

from views import debug_permits, run_work

urlpatterns = [
    path("work", run_work),
    path("_debug/permits", debug_permits),
]
