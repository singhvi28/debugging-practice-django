from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import reset, try_consume


@require_http_methods(["GET"])
def get_resource(request):
    client_id = request.headers.get("X-Client-Id", "")
    if not try_consume(client_id):
        return JsonResponse({"detail": "rate limit exceeded"}, status=429)
    return JsonResponse({"client_id": client_id, "status": "ok"})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})
