from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import check_rate_limit, reset


@require_http_methods(["GET"])
def search(request):
    user_id = request.headers.get("X-User-Id", "")
    route = request.path
    if not check_rate_limit(user_id, route):
        return JsonResponse({"detail": "rate limit exceeded"}, status=429)
    return JsonResponse({"user_id": user_id, "results": []})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})
