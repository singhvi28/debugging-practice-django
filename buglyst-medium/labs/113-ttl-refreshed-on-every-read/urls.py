from django.urls import path

from views import advance_clock, read_cache, write_cache

urlpatterns = [
    path("cache", write_cache),
    path("cache/<str:key>", read_cache),
    path("_test/clock", advance_clock),
]
