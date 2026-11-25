import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import verify

_processed: list[str] = []


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook(request):
    try:
        timestamp = int(request.headers.get("X-Signature-Timestamp", ""))
    except ValueError:
        return JsonResponse({"detail": "invalid or stale signature"}, status=401)
    signature = request.headers.get("X-Signature", "")
    body = request.body
    if not verify(timestamp, signature, body):
        return JsonResponse({"detail": "invalid or stale signature"}, status=401)
    payload = json.loads(body)
    event_id = payload["event_id"]
    _processed.append(event_id)
    return JsonResponse({"status": "processed", "event_id": event_id})


@require_http_methods(["GET"])
def debug_processed(request):
    return JsonResponse({"processed": list(_processed)})
