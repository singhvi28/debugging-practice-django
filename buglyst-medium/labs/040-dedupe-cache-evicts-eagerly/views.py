import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import processed_events, register_event


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook(request):
    try:
        event = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)

    event_id = event["event_id"]
    is_new = register_event(event_id)
    if not is_new:
        return JsonResponse({"status": "duplicate", "event_id": event_id})
    return JsonResponse({"status": "processed", "event_id": event_id})


@require_http_methods(["GET"])
def debug_processed(request):
    return JsonResponse({"processed": processed_events()})
