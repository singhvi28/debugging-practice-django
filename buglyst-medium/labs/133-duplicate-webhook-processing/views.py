import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from webhooks import dispatch, processed_events, record_processed, register_listener


def _handle(event: dict) -> None:
    record_processed(event["event_id"])


@csrf_exempt
@require_http_methods(["POST"])
def receive_webhook(request):
    event = json.loads(request.body)
    register_listener(_handle)
    handled_by = dispatch(event)
    return JsonResponse({"event_id": event["event_id"], "listeners": handled_by})


@require_http_methods(["GET"])
def debug_processed(request):
    return JsonResponse({"processed": processed_events()})
