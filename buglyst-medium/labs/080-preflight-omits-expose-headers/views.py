from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def profile(request):
    response = HttpResponse('{"user":"demo"}', content_type="application/json")
    response["X-Request-Id"] = "req-42"
    response["X-RateLimit-Remaining"] = "9"
    return response
