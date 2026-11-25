import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import create_session, validate_session


@csrf_exempt
@require_http_methods(["POST"])
def issue_session(request):
    body = json.loads(request.body)
    token = create_session(body["subject"], body.get("ttl_seconds", 3600))
    return JsonResponse({"token": token})


@require_http_methods(["GET"])
def me(request):
    authorization = request.META.get("HTTP_AUTHORIZATION")
    if not authorization or not authorization.startswith("Bearer "):
        return JsonResponse({"detail": "Missing bearer token"}, status=401)
    token = authorization.removeprefix("Bearer ").strip()
    session = validate_session(token)
    if session is None:
        return JsonResponse({"detail": "Invalid or expired session"}, status=401)
    return JsonResponse({"subject": session["subject"]})
