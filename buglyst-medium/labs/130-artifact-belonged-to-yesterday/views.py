import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from artifacts import upload_artifact


@csrf_exempt
@require_http_methods(["POST"])
def post_artifact(request):
    body = json.loads(request.body)
    run_id = body["run_id"]
    filename = body["filename"]
    url = upload_artifact(run_id, filename)
    return JsonResponse({"run_id": run_id, "url": url})
