import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from cache_helper import cache_miss, get_record, is_cached, put_record, reset

_db: dict[str, str] = {}


def reset_all() -> None:
    _db.clear()
    reset()


def _read_record(key):
    if is_cached(key):
        cached = get_record(key)
        if cached is None:
            return JsonResponse({"detail": "not found"}, status=404)
        return JsonResponse({"key": key, "value": cached})

    if key not in _db:
        cache_miss(key)
        return JsonResponse({"detail": "not found"}, status=404)

    value = _db[key]
    put_record(key, value)
    return JsonResponse({"key": key, "value": value})


def _create_record(request, key):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)
    _db[key] = body["value"]
    return JsonResponse({"key": key, "value": body["value"]})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def record_handler(request, key):
    if request.method == "GET":
        return _read_record(key)
    return _create_record(request, key)
