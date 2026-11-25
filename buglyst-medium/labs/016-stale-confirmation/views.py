import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from store import read_item, write_item


@require_http_methods(["GET"])
def get_item(request, item_id):
    try:
        return JsonResponse({"id": item_id, "value": read_item(item_id)})
    except KeyError:
        return JsonResponse({"detail": "not found"}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def put_item(request, item_id):
    body = json.loads(request.body)
    try:
        write_item(item_id, body["value"])
    except KeyError:
        return JsonResponse({"detail": "not found"}, status=404)
    return JsonResponse({"id": item_id, "value": read_item(item_id)})


@csrf_exempt
def item_detail(request, item_id):
    if request.method == "GET":
        return get_item(request, item_id)
    if request.method == "PUT":
        return put_item(request, item_id)
    return JsonResponse({"detail": "method not allowed"}, status=405)
