import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import AmountMismatchError, lookup, next_charge_id, save


@csrf_exempt
@require_http_methods(["POST"])
def create_payment(request):
    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        return JsonResponse({"detail": "Idempotency-Key required"}, status=400)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)

    amount = body.get("amount")
    currency = body.get("currency", "USD")

    try:
        existing = lookup(idempotency_key, amount)
    except AmountMismatchError:
        return JsonResponse(
            {"detail": "idempotency key reused with different amount"}, status=409
        )
    if existing is not None:
        return JsonResponse(existing)

    if amount is None or amount <= 0:
        return JsonResponse({"detail": "amount must be positive"}, status=400)

    record = {
        "idempotency_key": idempotency_key,
        "charge_id": next_charge_id(),
        "amount": amount,
        "currency": currency,
        "status": "created",
    }
    save(idempotency_key, record)
    return JsonResponse(record)
