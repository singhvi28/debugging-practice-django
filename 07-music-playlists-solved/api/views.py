from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def tracks_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_tracks(search), safe=False, status=200)

    body = parse_json(request)
    title = body.get("title", "")
    artist = body.get("artist", "")
    if not title or not artist:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    track = store.create_track(title, artist)
    return JsonResponse(track, status=201)


@require_http_methods(["GET"])
def get_track(request, track_id: str):
    track = store.get_track(track_id)
    if track is None:
        return JsonResponse({"detail": "Track not found"}, status=404)
    return JsonResponse(track, safe=False, status=200)


@require_http_methods(["GET"])
def get_playlist(request, playlist_id: str):
    playlist = store.get_playlist(playlist_id)
    if playlist is None:
        return JsonResponse({"detail": "Playlist not found"}, status=404)
    return JsonResponse(playlist)


@csrf_exempt
@require_http_methods(["POST"])
def add_track_to_playlist(request, playlist_id: str):
    body = parse_json(request)
    track_id = body.get("track_id")
    if not track_id:
        return JsonResponse({"detail": "track_id required"}, status=400)

    if store.get_track(track_id) is None:
        return JsonResponse({"detail": "Track not found"}, status=404)

    playlist = store.add_track_to_playlist(playlist_id, track_id)
    if playlist is None:
        return JsonResponse({"detail": "Track already in playlist"}, status=409)
    return JsonResponse(playlist, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_track_from_playlist(request, playlist_id: str, track_id: str):
    playlist = store.get_playlist(playlist_id)
    if playlist is None:
        return JsonResponse({"detail": "Playlist not found"}, status=404)
    if track_id not in playlist["track_ids"]:
        return JsonResponse({"detail": "Track not in playlist"}, status=404)
    store.remove_track_from_playlist(playlist_id, track_id)
    return HttpResponse(status=204)
