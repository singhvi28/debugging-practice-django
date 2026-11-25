import json

from django.http import JsonResponse

VALID_TOKEN = "secret-token"


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        token = auth.removeprefix("Bearer ").strip()
        if token != VALID_TOKEN:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        return JsonResponse({"detail": "Unauthorized"}, status=401)


def parse_json(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
