from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from backoff_helper import compute_delay_ms


@require_http_methods(["GET"])
def get_backoff(request, attempt):
    delay = compute_delay_ms(int(attempt))
    return JsonResponse({"attempt": int(attempt), "delay_ms": delay})
