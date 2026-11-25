from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from metrics import compute_p95, get_service_samples


@require_http_methods(["GET"])
def latency_metrics(request):
    samples = get_service_samples()
    p95 = compute_p95(samples)
    return JsonResponse({"p95_ms": p95, "services": list(samples.keys())})
