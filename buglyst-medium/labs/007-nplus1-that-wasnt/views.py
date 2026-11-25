from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from store import get_query_count, get_work_units, list_orders, load_items_for_order


@require_http_methods(["GET"])
def orders(request):
    result = []
    for order in list_orders():
        order["items"] = load_items_for_order(order["id"])
        result.append(order)
    return JsonResponse({"orders": result})


@require_http_methods(["GET"])
def debug_work_units(request):
    return JsonResponse({"work_units": get_work_units()})


@require_http_methods(["GET"])
def debug_query_count(request):
    return JsonResponse({"queries": get_query_count()})
