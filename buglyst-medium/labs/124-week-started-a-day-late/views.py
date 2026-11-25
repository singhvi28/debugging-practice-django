import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from buckets import bucket_event


@csrf_exempt
@require_http_methods(["POST"])
def bucket(request):
    body = json.loads(request.body)
    event_date = body["event_date"]
    week = bucket_event(event_date)
    return JsonResponse({"event_date": event_date, "week_start": week})
