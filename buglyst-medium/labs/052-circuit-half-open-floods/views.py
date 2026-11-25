from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from circuit_helper import (
    allow_request,
    circuit_state,
    half_open_probe_count,
    record_failure,
    record_success,
    reset_circuit,
    trip_to_half_open,
)

_downstream_calls = 0


def reset() -> None:
    global _downstream_calls
    _downstream_calls = 0
    reset_circuit()


def _call_downstream() -> dict:
    global _downstream_calls
    _downstream_calls += 1
    return {"status": "ok", "downstream_calls": _downstream_calls}


@csrf_exempt
@require_http_methods(["POST"])
def proxy_request(request):
    if not allow_request():
        return JsonResponse({"detail": "circuit open"}, status=503)
    try:
        return JsonResponse(_call_downstream())
    except Exception:
        record_failure()
        return JsonResponse({"detail": "downstream error"}, status=502)


@csrf_exempt
@require_http_methods(["POST"])
def proxy_success(request):
    if not allow_request():
        return JsonResponse({"detail": "circuit open"}, status=503)
    result = _call_downstream()
    record_success()
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def admin_half_open(request):
    trip_to_half_open()
    return JsonResponse({"state": circuit_state()})


@require_http_methods(["GET"])
def get_circuit(request):
    return JsonResponse({
        "state": circuit_state(),
        "half_open_probes": half_open_probe_count(),
    })


@require_http_methods(["GET"])
def debug_downstream_calls(request):
    return JsonResponse({"calls": _downstream_calls})
