from django.contrib import admin
from .models import Movie, Review, Watchlist


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "rating")
    list_filter = ("rating",)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
