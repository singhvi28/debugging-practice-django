import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import deduct, inventory_snapshot, list_orders, reset, save_order


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    body = json.loads(request.body)
    items = body["items"]
    order_id = f"ord-{len(list_orders()) + 1}"
    line_items = list(items)

    save_order(order_id, line_items)

    try:
        for item in items:
            deduct(item["sku"], item["quantity"])
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    return JsonResponse({"order_id": order_id, "status": "confirmed"})


@require_http_methods(["GET"])
def get_orders(request):
    return JsonResponse({"orders": list_orders()})


@require_http_methods(["GET"])
def get_inventory(request):
    return JsonResponse(inventory_snapshot())


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})


@csrf_exempt
def orders_endpoint(request):
    if request.method == "POST":
        return create_order(request)
    if request.method == "GET":
        return get_orders(request)
    return JsonResponse({"detail": "method not allowed"}, status=405)
