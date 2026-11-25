from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@require_http_methods(["GET"])
def list_accounts(request):
    return JsonResponse(store.list_accounts(), safe=False)


@require_http_methods(["GET"])
def get_account(request, account_id: str):
    account = store.get_account(account_id)
    if account is None:
        return JsonResponse({"detail": "Account not found"}, status=404)
    return JsonResponse(account)


@require_http_methods(["GET"])
def get_balance(request, account_id: str):
    balance = store.get_balance(account_id)
    if balance is None:
        return JsonResponse({"detail": "Account not found"}, status=404)
    return JsonResponse({"account_id": account_id, "balance": balance})


@csrf_exempt
@require_http_methods(["POST"])
def earn_points(request, account_id: str):
    body = parse_json(request)
    amount = body.get("amount")
    reason = body.get("reason", "")
    if amount is None or amount <= 0:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    account = store.earn_points(account_id, int(amount), reason)
    return JsonResponse(account, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def redeem_points(request):
    body = parse_json(request)
    account_id = request.GET.get("account_id", "")
    amount = body.get("amount")
    reason = body.get("reason", "")
    if not account_id or amount is None or amount <= 0:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    account = store.redeem_points(account_id, int(amount), reason)
    if account is None:
        return JsonResponse({"detail": "Account not found"}, status=404)
    return JsonResponse(account)


@require_http_methods(["GET"])
def get_ledger(request, account_id: str):
    ledger = store.get_ledger(account_id)
    if ledger is None:
        return JsonResponse({"detail": "Account not found"}, status=404)
    return JsonResponse(ledger, safe=False)
