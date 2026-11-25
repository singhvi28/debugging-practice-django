import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from payment import PaymentError, PaymentRequest, charge


@csrf_exempt
@require_http_methods(["POST"])
def post_charge(request):
    body = json.loads(request.body)
    authorization = request.headers.get("Authorization", "")
    payment_request = PaymentRequest(
        amount_cents=body["amount_cents"],
        authorization=authorization,
    )
    try:
        return JsonResponse(charge(payment_request))
    except PaymentError as exc:
        return JsonResponse({"detail": str(exc)}, status=402)
