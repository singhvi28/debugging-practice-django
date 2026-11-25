import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import verify_signature

_processed: list[str] = []


def _reset_processed() -> None:
    _processed.clear()


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook(request):
    body = request.body
    signature = request.META.get("HTTP_X_SIGNATURE")
    if not verify_signature(signature, body):
        return JsonResponse({"detail": "invalid signature"}, status=401)
    payload = json.loads(body)
    event_id = payload["event_id"]
    _processed.append(event_id)
    return JsonResponse({"status": "processed", "event_id": event_id})


@require_http_methods(["GET"])
def debug_processed(request):
    return JsonResponse({"processed": list(_processed)})


_reset_processed()
