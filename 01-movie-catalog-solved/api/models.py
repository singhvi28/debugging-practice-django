from django.db import models


class Movie(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.year})"


class Review(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.movie_id} - {self.rating} stars"


class Watchlist(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, related_name="watchlists", blank=True)

    def __str__(self):
        return self.name
