import json

from django.http import JsonResponse

VALID_TOKEN = "secret-token"


class AuthMiddleware:
    MUTATING_PREFIXES = ("/transfer", "/transfers")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        method = request.method.upper()

        needs_auth = method in ("POST", "PUT", "PATCH", "DELETE") and any(
            path.startswith(prefix) for prefix in self.MUTATING_PREFIXES
        )
        if not needs_auth:
            return self.get_response(request)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        token = auth.removeprefix("Bearer ").strip()
        if token != VALID_TOKEN:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        return self.get_response(request)


def parse_json(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
