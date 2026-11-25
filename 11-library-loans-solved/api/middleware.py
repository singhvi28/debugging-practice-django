import json

from django.http import JsonResponse

VALID_TOKEN = "secret-token"
ADMIN_TOKEN = "admin-token"


class AuthMiddleware:
    """Require Bearer token for borrowing; admin token for overdue list."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        method = request.method.upper()

        if method == "GET" and path == "/loans/overdue":
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            token = auth.removeprefix("Bearer ").strip()
            if token not in ADMIN_TOKEN:
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            return self.get_response(request)

        if method == "POST" and path == "/loans":
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            token = auth.removeprefix("Bearer ").strip()
            if token != VALID_TOKEN:
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            return self.get_response(request)

        return self.get_response(request)


def parse_json(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
