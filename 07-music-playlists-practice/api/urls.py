from django.urls import path

from api import views

urlpatterns = [
    path("tracks", views.tracks_collection),
    path("tracks/<str:track_id>", views.get_track),
    path("playlists/<str:playlist_id>", views.get_playlist),
    path("playlists/<str:playlist_id>/track", views.add_track_to_playlist),
    path(
        "playlists/<str:playlist_id>/tracks/<str:track_id>",
        views.remove_track_from_playlist,
    ),
]
