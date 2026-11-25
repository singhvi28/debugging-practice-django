import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from jobs import process_jobs, processed_jobs


@csrf_exempt
@require_http_methods(["POST"])
def run_jobs(request):
    body = json.loads(request.body)
    payload = body["jobs"]
    completed = process_jobs(payload)
    return JsonResponse({"completed": completed})


@require_http_methods(["GET"])
def debug_processed(request):
    return JsonResponse({"processed": processed_jobs()})
