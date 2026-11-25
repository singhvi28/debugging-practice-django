from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import current_schema, run_migrations


@csrf_exempt
@require_http_methods(["POST"])
def migrate(request):
    version = request.GET.get("version", "")
    return JsonResponse(run_migrations(version))


@require_http_methods(["GET"])
def schema(request):
    return JsonResponse({"columns": sorted(current_schema())})
