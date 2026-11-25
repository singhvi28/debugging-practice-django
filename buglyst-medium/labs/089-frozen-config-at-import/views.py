from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import feature_beta_enabled


@require_http_methods(["GET"])
def features(request):
    return JsonResponse({"feature_beta": feature_beta_enabled()})


@require_http_methods(["GET"])
def beta_endpoint(request):
    if not feature_beta_enabled():
        return JsonResponse({"enabled": False})
    return JsonResponse({"enabled": True, "payload": "beta-data"})
