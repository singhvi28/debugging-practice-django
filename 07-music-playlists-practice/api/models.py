from django.db import models


class Track(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in seconds")

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Playlist(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(Track, related_name="playlists", blank=True)

    def __str__(self):
        return self.name
