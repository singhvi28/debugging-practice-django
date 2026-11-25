from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from config import get_config


@require_http_methods(["GET"])
def read_config(request):
    return JsonResponse(get_config())
