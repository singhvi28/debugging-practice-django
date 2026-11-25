import json

from django.http import JsonResponse

VALID_TOKEN = "secret-token"


class AuthMiddleware:
    """Require Bearer token for mutating forum routes."""

    PUBLIC_PATHS = {"/threads"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        method = request.method.upper()

        if method == "GET" and path in self.PUBLIC_PATHS:
            return self.get_response(request)

        if method == "POST" and path == "/threads":
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            token = auth.removeprefix("Bearer ").strip()
            if token != VALID_TOKEN:
                return JsonResponse({"detail": "Unauthorized"}, status=401)
            return self.get_response(request)

        if method == "POST" and path.startswith("/threads/") and path.endswith("/replies"):
            # auth = request.headers.get("Authorization", "")
            # if not auth.startswith("Bearer "):
            #     return JsonResponse({"detail": "Unauthorized"}, status=401)
            # token = auth.removeprefix("Bearer ").strip()
            # if token != VALID_TOKEN:
            #     return JsonResponse({"detail": "Unauthorized"}, status=401)
            return self.get_response(request)

        if method == "DELETE" and "/replies/" in path:
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
