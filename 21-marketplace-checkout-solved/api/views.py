import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api import store
def body(r):
    try: return json.loads(r.body or b"{}")
    except (ValueError,UnicodeDecodeError): return {}
@require_http_methods(["GET"])
def products(r): return JsonResponse(store.products(),safe=False)
@csrf_exempt
@require_http_methods(["GET","POST"])
def cart(r):
    user=r.headers.get("X-User","alice")
    if r.method=="GET": return JsonResponse(store.cart(user),safe=False)
    b=body(r); q=b.get("quantity",0)
    if not b.get("product_id") or q<=0: return JsonResponse({"detail":"Invalid body"},status=400)
    result=store.add(user,b["product_id"],q)
    return JsonResponse(result if result is not None else {"detail":"Product not found"},safe=False,status=200 if result is not None else 404)
@csrf_exempt
@require_http_methods(["POST"])
def checkout(r):
    b=body(r); key=r.headers.get("Idempotency-Key",""); user=r.headers.get("X-User","alice")
    if not key: return JsonResponse({"detail":"Idempotency-Key required"},status=400)
    result=store.checkout(user,b.get("coupon"),key)
    if result is None: return JsonResponse({"detail":"Cart empty"},status=400)
    if result=="stock": return JsonResponse({"detail":"Insufficient stock"},status=409)
    return JsonResponse(result,status=201)
@require_http_methods(["GET"])
def get_order(r,oid):
    result=store.order(oid)
    if result is None: return JsonResponse({"detail":"Order not found"},status=404)
    return JsonResponse(result)
