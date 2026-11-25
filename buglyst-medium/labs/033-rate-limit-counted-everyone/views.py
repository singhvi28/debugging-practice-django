from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import check_rate_limit, reset


@require_http_methods(["GET"])
def api_data(request):
    tenant_id = request.META.get("HTTP_X_TENANT_ID", "")
    if not check_rate_limit(tenant_id):
        return JsonResponse({"detail": "rate limit exceeded"}, status=429)
    return JsonResponse({"tenant": tenant_id, "ok": True})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})
