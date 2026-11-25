"""In-memory movie catalog store."""

from __future__ import annotations

from copy import deepcopy

_movies: dict[str, dict] = {}
_reviews: dict[str, list[dict]] = {}
_watchlists: dict[str, dict] = {}


def reset() -> None:
    global _movies, _reviews, _watchlists
    _movies = {
        "m1": {"id": "m1", "title": "Interstellar", "year": 2014},
        "m2": {"id": "m2", "title": "Inception", "year": 2010},
        "m3": {"id": "m3", "title": "The Dark Knight", "year": 2008},
    }
    _reviews = {
        "m1": [{"id": "r1", "movie_id": "m1", "rating": 5, "text": "Masterpiece"}],
        "m2": [],
        "m3": [],
    }
    _watchlists = {
        "w1": {"id": "w1", "name": "Favorites", "movie_ids": ["m1"]},
    }


def list_movies(search: str | None = None) -> list[dict]:
    movies = list(_movies.values())
    if not search:
        return deepcopy(movies)
    return deepcopy([m for m in movies if search.lower() in m["title"].lower()])


def get_movie(movie_id: str) -> dict | None:
    movie = _movies.get(movie_id)
    return deepcopy(movie) if movie else None


def create_movie(title: str, year: int) -> dict:
    movie_id = f"m{len(_movies) + 1}"
    movie = {"id": movie_id, "title": title, "year": year}
    _movies[movie_id] = movie
    _reviews[movie_id] = []
    return deepcopy(movie)


def delete_movie(movie_id: str) -> bool:
    if movie_id not in _movies:
        return False
    del _movies[movie_id]
    _reviews.pop(movie_id, None)
    return True


def add_review(movie_id: str, rating: int, text: str) -> dict:
    review_id = f"r{sum(len(v) for v in _reviews.values()) + 1}"
    review = {"id": review_id, "movie_id": movie_id, "rating": rating, "text": text}
    _reviews.setdefault(movie_id, []).append(review)
    return deepcopy(review)


def get_watchlist(watch_list_id: str) -> dict | None:
    wl = _watchlists.get(watch_list_id)
    return deepcopy(wl) if wl else None


def add_movie_to_watchlist(watch_list_id: str, movie_id: str) -> dict | None:
    wl = _watchlists.get(watch_list_id)
    if wl is None:
        return None
    if movie_id in wl["movie_ids"]:
        return None
    wl["movie_ids"].append(movie_id)
    return deepcopy(wl)


reset()
