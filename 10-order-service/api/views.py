from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_products(request):
    search = request.GET.get("search")
    return JsonResponse(store.list_products(search), safe=False)


@require_http_methods(["GET"])
def get_product(request, product_id: str):
    product = store.get_product(product_id)
    if product is None:
        return JsonResponse({"detail": "Product not found"}, status=404)
    return JsonResponse(product)


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    body = parse_json(request)
    product_id = body.get("product_id")
    quantity = body.get("quantity")
    if not product_id or quantity is None:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    if store.get_product(product_id) is None:
        return JsonResponse({"detail": "Product not found"}, status=404)

    order = store.create_order(product_id, int(quantity))
    if order is None:
        return JsonResponse({"detail": "Product not found"}, status=404)
    return JsonResponse(order)


@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def order_detail(request, order_id: str):
    if request.method == "GET":
        order = store.get_order(order_id)
        return JsonResponse(order, safe=False)

    if not store.delete_order(order_id):
        return JsonResponse({"detail": "Order not found"}, status=404)
    return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(["PUT"])
def update_order_status(request, order_id: str):
    body = parse_json(request)
    status = body.get("status")
    if not status:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    order = store.update_order_status(order_id, status)
    if order is None:
        return JsonResponse({"detail": "Order not found"}, status=404)
    return JsonResponse(order)
