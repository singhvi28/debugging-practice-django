from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import maintenance_enabled


@require_http_methods(["GET"])
def status(request):
    return JsonResponse({"maintenance_mode": maintenance_enabled()})


@require_http_methods(["GET"])
def work(request):
    if maintenance_enabled():
        return JsonResponse({"detail": "maintenance in progress"}, status=503)
    return JsonResponse({"status": "ok"})
