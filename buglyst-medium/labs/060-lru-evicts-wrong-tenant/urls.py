from django.urls import path

from views import cache_entry, list_keys

urlpatterns = [
    path("cache/<str:tenant>/_keys", list_keys),
    path("cache/<str:tenant>/<str:key>", cache_entry),
]
