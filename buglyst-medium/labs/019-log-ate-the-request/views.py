import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from logging_helper import log_upload

logging.basicConfig(level=logging.DEBUG)


@csrf_exempt
@require_http_methods(["POST"])
def upload(request):
    body = request.body
    log_upload(body)
    return JsonResponse({"received": True, "bytes": len(body)})
