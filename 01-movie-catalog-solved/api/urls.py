from django.urls import path

from api import views

urlpatterns = [
    path("movies", views.movies_collection),
    path("movies/<str:movie_id>", views.movie_detail),
    path("movies/<str:movie_id>/reviews", views.create_review),
    path("watchlists/<str:watch_list_id>", views.get_watchlist),
    path("watchlists/<str:watch_list_id>/movies", views.add_to_watchlist),
]
