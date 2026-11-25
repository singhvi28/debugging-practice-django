import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from swr_helper import fetch_count, get_value, reset


@require_http_methods(["GET"])
def read_cache(request, key):
    return JsonResponse({"key": key, "value": get_value(key)})


@require_http_methods(["GET"])
def debug_fetch_count(request, key):
    return JsonResponse({"key": key, "fetches": fetch_count(key)})


@csrf_exempt
@require_http_methods(["POST"])
def debug_wait_stale(request):
    time.sleep(0.08)
    return JsonResponse({"status": "waited"})
