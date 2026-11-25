from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from cache import get


@require_http_methods(["GET"])
def report(request):
    return JsonResponse({"value": get("report")})


@require_http_methods(["GET"])
def debug_fetches(request):
    from backend import get_fetch_count

    return JsonResponse({"fetches": get_fetch_count()})
