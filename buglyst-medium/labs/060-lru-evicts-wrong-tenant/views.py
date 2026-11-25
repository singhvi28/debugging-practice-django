import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from lru_helper import get, keys, put


@require_http_methods(["GET"])
def list_keys(request, tenant):
    return JsonResponse({"tenant": tenant, "keys": keys(tenant)})


def _upsert(request, tenant, key):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)
    put(tenant, key, body["value"])
    return JsonResponse({"tenant": tenant, "key": key, "value": body["value"]})


def _read(tenant, key):
    value = get(tenant, key)
    if value is None:
        return JsonResponse({"detail": "not found"}, status=404)
    return JsonResponse({"tenant": tenant, "key": key, "value": value})


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def cache_entry(request, tenant, key):
    if request.method == "GET":
        return _read(tenant, key)
    return _upsert(request, tenant, key)
