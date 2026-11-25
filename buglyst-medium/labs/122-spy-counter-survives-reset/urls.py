from django.urls import path

from views import debug_spy, notify, reset

urlpatterns = [
    path("notify/<str:channel>", notify),
    path("_test/reset", reset),
    path("_debug/spy", debug_spy),
]
