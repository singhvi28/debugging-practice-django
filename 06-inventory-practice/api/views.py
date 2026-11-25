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

    store.create_product(name, int(qty))
    return JsonResponse(
        {"id": f"pr{len(store.list_products()) + 1}", "name": name, "qty": int(qty)},
        status=201,
    )


@require_http_methods(["GET"])
def get_product(request, product_id: str):
    product = store.get_product(product_id)
    return JsonResponse(product, safe=False)


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
        return JsonResponse({"detail": "Product not found"}, status=404)
    return JsonResponse(updated)


@require_http_methods(["GET"])
def list_moves(request, product_id: str):
    moves = store.list_moves(product_id)
    if moves is None:
        return JsonResponse({"detail": "Product not found"}, status=404)
    return JsonResponse(moves, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id: str):
    if not store.delete_product(product_id):
        return JsonResponse({"detail": "Product not found"}, status=404)
    return HttpResponse(status=204)
