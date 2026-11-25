from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from client import call_upstream


@require_http_methods(["GET"])
def get_data(request):
    try:
        return JsonResponse(call_upstream())
    except TimeoutError:
        return JsonResponse({"detail": "upstream timeout"}, status=504)
