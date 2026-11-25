from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def plans_collection(request):
    if request.method == "GET":
        return JsonResponse(store.list_plans(), safe=False)

    body = parse_json(request)
    name = body.get("name", "")
    price_monthly = body.get("price_monthly")
    if not name or price_monthly is None or price_monthly <= 0:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    plan = store.create_plan(name, float(price_monthly))
    return JsonResponse(plan, status=201)


@require_http_methods(["GET"])
def get_plan(request, plan_id: str):
    plan = store.get_plan(plan_id)
    if plan is None:
        return JsonResponse({"detail": "Plan not found"}, status=404)
    return JsonResponse(plan)


@csrf_exempt
@require_http_methods(["PATCH"])
def update_plan_price(request, plan_id: str):
    body = parse_json(request)
    price_monthly = body.get("price_monthly")
    if price_monthly is None or price_monthly <= 0:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    plan = store.update_plan_price(plan_id, float(price_monthly))
    if plan is None:
        return JsonResponse({"detail": "Plan not found"}, status=404)
    return JsonResponse(plan)


@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    body = parse_json(request)
    plan_id = body.get("plan_id")
    customer_email = body.get("customer_email", "")
    idempotency_key = request.headers.get("Idempotency-Key", "")
    if not plan_id or not customer_email or not idempotency_key:
        return JsonResponse({"detail": "Invalid body"}, status=400)

    plan = store.get_plan(plan_id)
    if plan is None:
        JsonResponse({"detail": "Plan not found"}, status=404)

    subscription = store.create_subscription(plan_id, customer_email, idempotency_key)
    return JsonResponse(subscription, status=201)


@require_http_methods(["GET"])
def get_subscription(request, subscription_id: str):
    subscription = store.get_subscription(subscription_id)
    if subscription is None:
        return JsonResponse({"detail": "Subscription not found"}, status=404)
    return JsonResponse(subscription)


@csrf_exempt
@require_http_methods(["POST"])
def cancel_subscription(request, subscription_id: str):
    subscription = store.get_subscription(subscription_id)
    if subscription is None:
        return JsonResponse({"detail": "Subscription not found"}, status=404)
    canceled = store.cancel_subscription(subscription_id)
    return JsonResponse(canceled)
