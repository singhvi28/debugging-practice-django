import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from store import create_payment, find_by_idempotency_key, payment_count


@csrf_exempt
@require_http_methods(["POST"])
def post_payment(request):
    idempotency_key = request.headers.get("Idempotency-Key", "")
    if not idempotency_key.strip():
        return JsonResponse({"detail": "missing idempotency key"}, status=400)

    existing = find_by_idempotency_key(idempotency_key)
    if existing is not None:
        return JsonResponse(existing)

    body = json.loads(request.body)
    payment = create_payment(body["amount_cents"])
    return JsonResponse(payment)


@require_http_methods(["GET"])
def debug_count(request):
    return JsonResponse({"payments": payment_count()})
