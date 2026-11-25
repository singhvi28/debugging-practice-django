from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from orders import list_orders


@require_http_methods(["GET"])
def get_orders(request):
    tenant_id = request.META.get("HTTP_X_TENANT_ID")
    if not tenant_id:
        return JsonResponse({"detail": "Missing X-Tenant-Id header"}, status=400)
    orders = list_orders(tenant_id)
    return JsonResponse({"tenant_id": tenant_id, "orders": orders})
