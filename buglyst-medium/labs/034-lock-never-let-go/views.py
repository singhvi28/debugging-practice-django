import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import is_locked, reset, run_with_lock


@csrf_exempt
@require_http_methods(["POST"])
def run_job(request):
    body = json.loads(request.body)
    resource = body["resource"]
    should_fail = body.get("should_fail", False)
    if is_locked(resource):
        return JsonResponse({"detail": "resource locked"}, status=423)
    try:
        run_with_lock(resource, should_fail)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=500)
    return JsonResponse({"resource": resource, "status": "completed"})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})
