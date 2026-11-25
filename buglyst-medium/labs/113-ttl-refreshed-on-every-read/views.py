import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from cache import get, put, set_clock


@csrf_exempt
@require_http_methods(["POST"])
def write_cache(request):
    body = json.loads(request.body)
    put(body["key"], body["value"], body["ttl_seconds"])
    return JsonResponse({"key": body["key"], "stored": True})


@require_http_methods(["GET"])
def read_cache(request, key):
    value = get(key)
    if value is None:
        return JsonResponse({"detail": "miss"}, status=404)
    return JsonResponse({"key": key, "value": value})


@csrf_exempt
@require_http_methods(["POST"])
def advance_clock(request):
    body = json.loads(request.body)
    set_clock(body["now"])
    return JsonResponse({"now": body["now"]})
