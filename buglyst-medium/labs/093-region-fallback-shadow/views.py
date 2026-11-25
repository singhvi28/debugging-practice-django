from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import resolve_region


@csrf_exempt
@require_http_methods(["POST"])
def deploy_region(request):
    region = request.GET.get("region")
    return JsonResponse(resolve_region(orchestrator_region=region))
