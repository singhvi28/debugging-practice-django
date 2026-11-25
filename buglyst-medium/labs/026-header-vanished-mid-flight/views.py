from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from forwarder import forward

_last_echoed_headers: dict[str, str] = {}


def _echo_handler(headers: dict[str, str]) -> dict:
    global _last_echoed_headers
    _last_echoed_headers = dict(headers)
    return {"received": headers}


@csrf_exempt
@require_http_methods(["POST"])
def proxy_forward(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    headers: dict[str, str] = {}
    if authorization:
        headers["Authorization"] = authorization
    headers["X-Request-Id"] = "req-1"
    result = forward(headers, _echo_handler)
    return JsonResponse(result)


@require_http_methods(["GET"])
def last_echo(request):
    return JsonResponse({"headers": _last_echoed_headers})
