from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def files_collection(request):
    if request.method == "GET":
        tag = request.GET.get("tag")
        return JsonResponse(store.list_files(tag), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    mime_type = body.get("mime_type", "")
    if not title or not mime_type:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    file = store.create_file(title, mime_type)
    return JsonResponse(file, status=201)


@csrf_exempt
@require_http_methods(["GET", "PATCH"])
def file_detail(request, file_id: str):
    if request.method == "GET":
        file = store.get_file(file_id)
        if file is None:
            return JsonResponse({"detail": "File not found"}, status=404)
        return JsonResponse(file, safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    if not title:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    if store.get_file(file_id) is None:
        return JsonResponse({"detail": "File not found"}, status=404)
    file = store.update_file(file_id, title)
    return JsonResponse(file, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def add_tag(request, file_id: str):
    file = store.get_file(file_id)
    if file is None:
        return JsonResponse({"detail": "File not found"}, status=404)
    body = parse_json(request)
    name = body.get("name", "")
    if not name:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    updated = store.add_tag(file_id, name)
    if updated is None:
        return JsonResponse({"detail": "Duplicate tag"}, status=409)
    return JsonResponse(updated)

