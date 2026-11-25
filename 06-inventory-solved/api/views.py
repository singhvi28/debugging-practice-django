from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
async def products_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_products(search), safe=False)

    body = parse_json(request)
    name = body.get("name", "")
    qty = body.get("qty")
    if not name or qty is None:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    product = await store.create_product(name, int(qty))
    if product is None:
        return JsonResponse({"detail": "Product already exists"}, status=400)
    return JsonResponse(product, status=201)


@require_http_methods(["GET", "DELETE"])
def get_product(request, product_id: str):
    if request.method == "GET":
        product = store.get_product(product_id)
        if product is None:
            return JsonResponse({"detail": "Product not found"}, status=404)
        return JsonResponse(product, safe=False)

    if request.method == "DELETE":
        if store.delete_product(product_id):
            return HttpResponse(status=204)
        return JsonResponse({"detail": "Product not found"}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def adjust_stock(request, product_id: str):
    if store.get_product(product_id) is None:
        return JsonResponse({"detail": "Product not found"}, status=404)

    body = parse_json(request)
    delta = body.get("delta")
    if delta is None or not isinstance(delta, int):
        return JsonResponse({"detail": "Invalid body"}, status=400)

    updated = store.adjust_stock(product_id, delta)
    if updated is None:
        return JsonResponse({"detail": "Qty after adjustment would be negative"}, status=400)
    return JsonResponse(updated)


@require_http_methods(["GET"])
def list_moves(request, product_id: str):
    moves = store.list_moves(product_id)
    if moves is None:
        return JsonResponse({"detail": "Product not found"}, status=404)
    return JsonResponse(moves, safe=False)
