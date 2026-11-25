from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import fetch_user_for_row, list_orders


@require_http_methods(["GET"])
def enriched_orders(request):
    rows = list_orders()
    enriched = []
    for row in rows:
        user = fetch_user_for_row(row)
        if user is None:
            continue
        enriched.append({"order_id": row.id, "user_id": user.id, "user_name": user.name})
    return JsonResponse({"orders": enriched, "count": len(enriched)})
