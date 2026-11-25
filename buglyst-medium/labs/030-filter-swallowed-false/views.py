from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from items import list_items, parse_include_deleted


@require_http_methods(["GET"])
def get_items(request):
    include = parse_include_deleted(request.GET.get("includeDeleted"))
    return JsonResponse({"items": list_items(include)})
