import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from events import emit_event, reconnect, webhook_deliveries


@csrf_exempt
@require_http_methods(["POST"])
def post_reconnect(request):
    reconnect()
    return JsonResponse({"reconnected": True})


@csrf_exempt
@require_http_methods(["POST"])
def post_event(request):
    body = json.loads(request.body)
    listener_count = emit_event(body)
    return JsonResponse({"delivered_to": listener_count})


@require_http_methods(["GET"])
def get_webhooks(request):
    return JsonResponse({"deliveries": webhook_deliveries()})
