from django.http import JsonResponse
TOKEN = "secret-token"
class AuthMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        if request.method in {"POST", "PATCH", "DELETE"} and request.path.startswith(("/checkout", "/orders")):
            if request.headers.get("Authorization") != f"Bearer {TOKEN}":
                return JsonResponse({"detail":"Unauthorized"}, status=401)
        return self.get_response(request)
