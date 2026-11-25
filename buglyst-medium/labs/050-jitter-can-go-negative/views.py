import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from jitter_helper import apply_jitter


@csrf_exempt
@require_http_methods(["POST"])
def compute_jitter(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "invalid json"}, status=400)

    base_ms = body.get("base_ms")
    jitter_ms = body.get("jitter_ms")
    seed = body.get("seed")

    if base_ms is None or base_ms <= 0:
        return JsonResponse({"detail": "base_ms must be positive"}, status=400)
    if jitter_ms is None or jitter_ms < 0:
        return JsonResponse({"detail": "jitter_ms must be non-negative"}, status=400)

    delay = apply_jitter(base_ms, jitter_ms, seed)
    return JsonResponse({
        "base_ms": base_ms,
        "jitter_ms": jitter_ms,
        "delay_ms": delay,
    })
