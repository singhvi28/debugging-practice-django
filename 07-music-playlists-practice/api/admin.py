from django.contrib import admin
from .models import Track, Playlist


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "duration")
    search_fields = ("title", "artist")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
