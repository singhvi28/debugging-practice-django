import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import fingerprint, lookup, next_operation_id, save


@csrf_exempt
@require_http_methods(["POST"])
def create_operation(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)

    for field in ("account", "amount"):
        if field not in payload:
            return JsonResponse({"detail": f"missing field: {field}"}, status=400)

    fp = fingerprint(payload)
    existing = lookup(fp)
    if existing is not None:
        return JsonResponse(existing)

    record = {
        "operation_id": next_operation_id(),
        "account": payload["account"],
        "amount": payload["amount"],
        "currency": payload.get("currency", "USD"),
        "status": "created",
    }
    save(fp, record)
    return JsonResponse(record)
