import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import decode_body


@csrf_exempt
@require_http_methods(["POST"])
def decode(request):
    body = json.loads(request.body)
    raw = bytes.fromhex(body["content"])
    text = decode_body(raw, body["content_type"])
    return JsonResponse({"text": text, "declared_charset": body["content_type"]})
