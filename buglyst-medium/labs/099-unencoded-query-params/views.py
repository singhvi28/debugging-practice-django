from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helper import build_url


@require_http_methods(["GET"])
def search_url(request):
    q = request.GET.get("q", "")
    city = request.GET.get("city", "New York")
    url = build_url("https://catalog.example/search", {"q": q, "city": city})
    return JsonResponse({"url": url})
