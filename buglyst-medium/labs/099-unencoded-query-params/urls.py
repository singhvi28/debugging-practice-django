from django.urls import path

from views import search_url

urlpatterns = [
    path("search-url", search_url),
]
