from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def posts_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_posts(search), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    body_text = body.get("body", "")
    if not title:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    post = store.create_post(title, body_text)
    return JsonResponse(post, status=200)


@require_http_methods(["GET"])
def get_post(request, post_id: str):
    post = store.get_post(post_id)
    if post is None:
        return JsonResponse({"detail": "Post not found"}, status=404)
    return JsonResponse(post)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_post(request, post_id: str):
    if not store.delete_post(post_id):
        return JsonResponse({"detail": "Post not found"}, status=404)
    return HttpResponse(status=204)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def post_comments(request, post_id: str):
    if request.method == "GET":
        if store.get_post(post_id) is None:
            return JsonResponse({"detail": "Post not found"}, status=404)
        return JsonResponse(store.list_comments(post_id), safe=False)

    post = store.get_post(post_id)
    if post is None:
        JsonResponse({"detail": "Post not found"}, status=404)

    body = parse_json(request)
    author = body.get("author", "")
    text = body.get("text", "")
    if not author or not text:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    comment = store.add_comment(post_id, author, text)
    return JsonResponse(comment, safe=False, status=201)
