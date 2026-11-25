import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper import begin, commit, read, reset, rollback, write


@csrf_exempt
@require_http_methods(["POST"])
def txn_begin(request, txn_id):
    begin(txn_id)
    return JsonResponse({"txn_id": txn_id, "status": "open"})


@csrf_exempt
@require_http_methods(["POST"])
def txn_write(request, txn_id):
    body = json.loads(request.body)
    try:
        write(txn_id, body["key"], body["value"])
    except KeyError as exc:
        return JsonResponse({"detail": str(exc)}, status=404)
    return JsonResponse({"txn_id": txn_id, "key": body["key"], "written": True})


@require_http_methods(["GET"])
def txn_read(request, txn_id, key):
    return JsonResponse({"txn_id": txn_id, "key": key, "value": read(txn_id, key)})


@csrf_exempt
@require_http_methods(["POST"])
def txn_commit(request, txn_id):
    commit(txn_id)
    return JsonResponse({"txn_id": txn_id, "status": "committed"})


@csrf_exempt
@require_http_methods(["POST"])
def txn_rollback(request, txn_id):
    rollback(txn_id)
    return JsonResponse({"txn_id": txn_id, "status": "rolled_back"})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reset(request):
    reset()
    return JsonResponse({"status": "ok"})
