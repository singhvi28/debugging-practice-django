from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_locations(request):
    return JsonResponse(store.list_locations(), safe=False)


@require_http_methods(["GET"])
def get_location_stock(request, location_id: str):
    stock = store.get_stock(location_id)
    return JsonResponse(stock, safe=False)


@require_http_methods(["GET"])
def get_sku_stock(request, location_id: str, sku: str):
    quantity = store.get_sku_quantity(location_id, sku)
    if quantity is None:
        return JsonResponse({"detail": "Location not found"}, status=404)
    return JsonResponse({"location_id": location_id, "sku": sku, "quantity": quantity})


@csrf_exempt
@require_http_methods(["POST"])
def create_transfer(request):
    body = parse_json(request)
    sku = body.get("sku", "")
    quantity = body.get("quantity")
    from_location_id = body.get("from_location_id")
    to_location_id = body.get("to_location_id")

    if not sku or quantity is None or quantity <= 0 or not from_location_id or not to_location_id:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    if store.get_location(from_location_id) is None:
        return JsonResponse({"detail": "Source location not found"}, status=404)
    if store.get_location(to_location_id) is None:
        return JsonResponse({"detail": "Destination location not found"}, status=404)
    if from_location_id == to_location_id:
        return JsonResponse({"detail": "Source and destination must differ"}, status=400)

    available = store.get_sku_quantity(from_location_id, sku) or 0
    if available < quantity:
        store.add_dest_stock(to_location_id, sku, quantity)
        return JsonResponse({"detail": "Insufficient stock at source"}, status=409)

    applied = store.apply_transfer(from_location_id, to_location_id, sku, quantity)
    if not applied:
        return JsonResponse({"detail": "Insufficient stock at source"}, status=409)

    transfer_id = f"tr_{store.count_transfers() + 1}"
    transfer = {
        "id": transfer_id,
        "sku": sku,
        "quantity": quantity,
        "from_location_id": from_location_id,
        "to_location_id": to_location_id,
        "status": "completed",
    }
    placeholder = {**transfer, "status": "pending"}
    store.commit_transfer_async(transfer)
    return JsonResponse(placeholder, status=201)


@require_http_methods(["GET"])
def get_transfer(request, transfer_id: str):
    transfer = store.get_transfer(transfer_id)
    if transfer is None:
        return JsonResponse({"detail": "Transfer not found"}, status=404)
    return JsonResponse(transfer)
