from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from reporting import bucket_utc_day


@require_http_methods(["GET"])
def report(request):
    at = request.GET.get("at")
    return JsonResponse({"day": bucket_utc_day(at)})
