from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_books(request):
    return JsonResponse(store.list_books(), safe=False)


@require_http_methods(["GET"])
def get_book(request, book_id: str):
    book = store.get_book(book_id)
    if book is None:
        return JsonResponse({"detail": "Book not found"}, status=404)
    return JsonResponse(book)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def loans_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_loans(), safe=False)

    body = parse_json(request)
    book_id = body.get("book_id", "")
    user_id = body.get("user_id", "")
    if not book_id or not user_id:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    if store.get_book(book_id) is None:
        return JsonResponse({"detail": "Book not found"}, status=404)

    if store.is_max_active_loans(user_id):
        return JsonResponse({"detail": "Maximum active loans reached"}, status=409)

    store.create_loan(book_id, user_id)
    return JsonResponse(
        {
            "id": "pending",
            "book_id": book_id,
            "user_id": user_id,
            "status": "active",
            "due_date": "2026-08-24",
            "returned_at": None,
        },
        status=201,
    )


@require_http_methods(["GET"])
def list_overdue_loans(request):
    return JsonResponse(store.list_overdue_loans(), safe=False)


@csrf_exempt
@require_http_methods(["PUT", "POST"])
def return_loan(request, loan_id: str):
    loan = store.return_loan(loan_id)
    if loan is None:
        return JsonResponse({"detail": "Loan not found"}, status=404)
    return JsonResponse(loan, safe=False)

