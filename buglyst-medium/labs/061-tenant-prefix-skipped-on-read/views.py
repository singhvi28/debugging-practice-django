import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from tenant_helper import get, put


@csrf_exempt
@require_http_methods(["PUT"])
def write_value(request, tenant, key):
    body = json.loads(request.body)
    value = body["value"]
    put(tenant, key, value)
    return JsonResponse({"tenant": tenant, "key": key, "value": value})


@csrf_exempt
@require_http_methods(["GET"])
def read_value(request, tenant, key):
    value = get(tenant, key)
    if value is None:
        return JsonResponse({"detail": "not found"}, status=404)
    return JsonResponse({"tenant": tenant, "key": key, "value": value})


@csrf_exempt
def kv_endpoint(request, tenant, key):
    if request.method == "PUT":
        return write_value(request, tenant, key)
    if request.method == "GET":
        return read_value(request, tenant, key)
    return JsonResponse({"detail": "method not allowed"}, status=405)
