from django.urls import path

from views import debug_fetch_count, debug_wait_stale, read_cache

urlpatterns = [
    path("cache/<str:key>", read_cache),
    path("_debug/fetch-count/<str:key>", debug_fetch_count),
    path("_debug/wait-stale", debug_wait_stale),
]
