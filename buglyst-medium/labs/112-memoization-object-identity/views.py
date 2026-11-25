import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import SearchQuery, search_catalog


@csrf_exempt
@require_http_methods(["POST"])
def search(request):
    body = json.loads(request.body)
    query = SearchQuery(term=body["term"], category=body["category"])
    return JsonResponse(search_catalog(query))
