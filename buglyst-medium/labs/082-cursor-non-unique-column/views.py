from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import paginate


@require_http_methods(["GET"])
def list_tasks(request):
    cursor = request.GET.get("cursor")
    limit = int(request.GET.get("limit", 2))
    limit = max(1, min(limit, 10))
    items, next_cursor = paginate(cursor, limit)
    return JsonResponse({"items": items, "next_cursor": next_cursor})
