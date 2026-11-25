from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import get_header

VALID_TOKEN = "service-token"


def _incoming_headers(request) -> dict[str, str]:
    """Plain header dict with caller casing (not Django's normalized HttpHeaders)."""
    headers: dict[str, str] = {}
    for key, value in request.META.items():
        if key.startswith("HTTP_"):
            name = key[5:].replace("_", "-").lower()
            headers[name] = value
    return headers


@require_http_methods(["GET"])
def protected(request):
    token = get_header(_incoming_headers(request), "Authorization")
    if token != f"Bearer {VALID_TOKEN}":
        return JsonResponse({"authorized": False})
    return JsonResponse({"authorized": True, "subject": "api-client"})
