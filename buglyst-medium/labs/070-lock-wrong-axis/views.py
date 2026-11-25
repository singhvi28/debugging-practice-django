import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import reset_locks, slot_lock


@csrf_exempt
@require_http_methods(["POST"])
def reserve(request):
    body = json.loads(request.body)
    caller_id = body["caller_id"]
    slot_id = body["slot_id"]
    with slot_lock(caller_id, slot_id):
        time.sleep(0.02)
    return JsonResponse({"caller_id": caller_id, "slot_id": slot_id, "reserved": True})


@csrf_exempt
@require_http_methods(["POST"])
def reset(request):
    reset_locks()
    return JsonResponse({"status": "ok"})
