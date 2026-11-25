from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def books_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_books(search), safe=False)

    body = parse_json(request)
    title = body.get("title", "")
    author = body.get("author", "")
    if not title or not author:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    book = store.create_book(title, author)
    return JsonResponse(book)


@require_http_methods(["GET"])
def get_book(request, book_id: str):
    book = store.get_book(book_id)
    return JsonResponse(book, safe=False)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, book_id: str):
    if not store.delete_book(book_id):
        return JsonResponse({"detail": "Book not found"}, status=404)
    return HttpResponse(status=204)


@require_http_methods(["GET"])
def get_cart(request, cart_id: str):
    cart = store.get_cart(cart_id)
    if cart is None:
        return JsonResponse({"detail": "Cart not found"}, status=404)
    return JsonResponse(cart)


@csrf_exempt
@require_http_methods(["POST"])
def add_cart_item(request, cart_id: str):
    body = parse_json(request)
    book_id = body.get("book_id")
    if not book_id:
        return JsonResponse({"detail": "book_id required"}, status=400)

    if store.get_book(book_id) is None:
        return JsonResponse({"detail": "Book not found"}, status=404)

    cart = store.add_to_cart(cart_id, book_id)
    if cart is None:
        return JsonResponse({"detail": "Cart not found"}, status=404)
    return JsonResponse(cart)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_cart_item(request, cart_id: str, book_id: str):
    if not store.remove_from_cart(cart_id, book_id):
        return JsonResponse({"detail": "Cart not found"}, status=404)
    return HttpResponse(status=204)
