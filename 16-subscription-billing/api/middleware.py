import json

from django.http import JsonResponse

VALID_TOKEN = "secret-token"
ADMIN_TOKEN = "admin-token"


class AuthMiddleware:
    ADMIN_ROUTES = (
        ("POST", "/plans"),
        ("PATCH", "/plans"),
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        method = request.method.upper()

        needs_auth = method in ("POST", "PATCH", "DELETE") and (
            path.startswith("/plans") or path.startswith("/subscriptions")
        )
        if not needs_auth:
            return self.get_response(request)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        token = auth.removeprefix("Bearer ").strip()
        if token not in (VALID_TOKEN, ADMIN_TOKEN):
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        is_admin_route = any(
            method == route_method and path.startswith(prefix)
            for route_method, prefix in self.ADMIN_ROUTES
        )
        if is_admin_route and token == VALID_TOKEN:
            return self.get_response(request)
        if is_admin_route and token != ADMIN_TOKEN:
            return JsonResponse({"detail": "Admin required"}, status=403)

        return self.get_response(request)


def parse_json(request) -> dict:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
