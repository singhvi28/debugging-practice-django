from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from retry_helper import call_with_retry
from upstream import ServiceUnavailable, call_upstream, get_attempts


@require_http_methods(["GET"])
def status(request):
    try:
        return JsonResponse(call_with_retry(call_upstream))
    except ServiceUnavailable:
        return JsonResponse({"detail": "upstream unavailable"}, status=503)


@require_http_methods(["GET"])
def debug_attempts(request):
    return JsonResponse({"attempts": get_attempts()})
