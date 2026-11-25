from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from budget_helper import (
    BudgetExhausted,
    TransientError,
    budget_remaining,
    reset_budget,
    run_with_budget,
)

_call_counts: dict[str, int] = {}
_failures: dict[str, int] = {}


def reset(caller_id: str, failures_before_success: int = 0) -> None:
    _call_counts[caller_id] = 0
    _failures[caller_id] = failures_before_success


def _flaky_call(caller_id: str) -> dict:
    _call_counts[caller_id] += 1
    if _call_counts[caller_id] <= _failures.get(caller_id, 0):
        raise TransientError("upstream unavailable")
    return {"caller": caller_id, "calls": _call_counts[caller_id]}


@csrf_exempt
@require_http_methods(["POST"])
def call_upstream(request, caller_id):
    failures_before_success = int(request.GET.get("failures_before_success", 0))
    reset(caller_id, failures_before_success)
    try:
        return JsonResponse(run_with_budget(lambda: _flaky_call(caller_id)))
    except BudgetExhausted:
        return JsonResponse({"detail": "retry budget exhausted"}, status=429)
    except TransientError:
        return JsonResponse({"detail": "upstream failed"}, status=503)


@require_http_methods(["GET"])
def get_budget(request):
    return JsonResponse({"remaining": budget_remaining()})


def init_budget() -> None:
    reset_budget()
