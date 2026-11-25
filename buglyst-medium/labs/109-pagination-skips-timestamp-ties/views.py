from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import page_after


@require_http_methods(["GET"])
def activities(request):
    cursor = request.GET.get("cursor")
    limit = int(request.GET.get("limit", "2"))
    limit = max(1, min(limit, 10))
    page = page_after(cursor, limit)
    return JsonResponse(
        {
            "items": [{"id": item.id, "updated_at": item.updated_at} for item in page],
            "next_cursor": page[-1].updated_at if page else None,
        }
    )
