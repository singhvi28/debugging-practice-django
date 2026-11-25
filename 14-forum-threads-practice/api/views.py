from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def threads_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_threads(), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    author = body.get("author", "")
    if not title or not author:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    thread = store.create_thread(title, author)
    return JsonResponse(thread, status=201)


@require_http_methods(["GET"])
def get_thread(request, thread_id: str):
    thread = store.get_thread(thread_id)
    if thread is None:
        return JsonResponse({"detail": "Thread not found"}, status=404)
    return JsonResponse(thread)


@require_http_methods(["GET"])
def list_deleted_threads(request):
    return JsonResponse(store.list_deleted_threads(), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def create_reply(request, thread_id: str):
    body = parse_json(request)
    author = body.get("author", "")
    body_text = body.get("body", "")
    if not author or not body_text:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    reply = store.create_reply(thread_id, author, body_text)
    if reply is None:
        return JsonResponse({"detail": "Thread not found"}, status=404)
    return JsonResponse(reply, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_reply(request, thread_id: str, reply_id: str):
    deleted = store.delete_reply(thread_id, reply_id)
    if not deleted:
        return JsonResponse({"detail": "Reply not found"}, status=404)
    return HttpResponse(status=204)

