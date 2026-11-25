import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import validate_next_url

VALID_PASSWORD = "secret"


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    body = json.loads(request.body)
    if body.get("password") != VALID_PASSWORD:
        return JsonResponse({"detail": "invalid credentials"}, status=401)
    try:
        redirect = validate_next_url(body.get("next", "/dashboard"))
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)
    return JsonResponse({"username": body["username"], "redirect": redirect})
