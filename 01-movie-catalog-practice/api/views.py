from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def movies_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_movies(search), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    year = body.get("year")
    if not title or year is None:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    movie = store.create_movie(title, int(year))
    return JsonResponse(movie, status=200)


@require_http_methods(["GET"])
def get_movie(request, movie_id: str):
    movie = store.get_movie(movie_id)
    return JsonResponse(movie)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_movie(request, movie_id: str):
    if not store.delete_movie(movie_id):
        return JsonResponse({"detail": "Movie not found"}, status=404)
    return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(["POST"])
def create_review(request, movie_id: str):
    body = parse_json(request)
    rating = body.get("rating")
    text = body.get("text", "")
    if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
        return JsonResponse({"detail": "Invalid rating"}, status=400)

    review = store.add_review(movie_id, rating, text)
    return JsonResponse(review, status=201)


@require_http_methods(["GET"])
def get_watchlist(request, watch_list_id: str):
    wl = store.get_watchlist(watch_list_id)
    if wl is None:
        return JsonResponse({"detail": "Watchlist not found"}, status=404)
    return JsonResponse(wl)


@csrf_exempt
@require_http_methods(["POST"])
def add_to_watchlist(request, watch_list_id: str):
    body = parse_json(request)
    movie_id = body.get("movie_id")
    if not movie_id:
        return JsonResponse({"detail": "movie_id required"}, status=400)

    if store.get_movie(movie_id) is None:
        return JsonResponse({"detail": "Movie not found"}, status=404)

    wl = store.get_watchlist(watch_list_id)
    if wl is None:
        return JsonResponse({"detail": "Watchlist not found"}, status=404)

    updated = store.add_movie_to_watchlist(watch_list_id, movie_id)
    return JsonResponse(updated)
