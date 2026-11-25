from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from semaphore import available_permits, with_lock


@csrf_exempt
@require_http_methods(["POST"])
def run_work(request):
    try:
        with_lock(lambda: {"done": True})
    except RuntimeError:
        return JsonResponse({"detail": "pool exhausted"}, status=503)
    return JsonResponse({"status": "ok"})


@require_http_methods(["GET"])
def debug_permits(request):
    return JsonResponse({"available": available_permits()})
