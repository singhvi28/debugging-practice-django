import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from xgroup import build_xgroup_args


@csrf_exempt
@require_http_methods(["POST"])
def build_args(request):
    body = json.loads(request.body)
    tokens = build_xgroup_args(
        body["command"],
        body["stream"],
        body["group"],
        body["stream_id"],
        entries_read=body.get("entries_read"),
        mkstream=body.get("mkstream", False),
    )
    return JsonResponse({"tokens": tokens})
