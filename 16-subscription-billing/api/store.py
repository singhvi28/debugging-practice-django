from copy import deepcopy

_plans = {
    "plan_basic": {"id": "plan_basic", "name": "Basic", "price_monthly": 9.99},
    "plan_pro": {"id": "plan_pro", "name": "Pro", "price_monthly": 19.99},
}

_subscriptions: dict[str, dict] = {}
_idempotency_index: dict[str, str] = {}
_plan_price_cache = {plan_id: plan["price_monthly"] for plan_id, plan in _plans.items()}


def reset() -> None:
    global _plans, _subscriptions, _idempotency_index, _plan_price_cache
    _plans = {
        "plan_basic": {"id": "plan_basic", "name": "Basic", "price_monthly": 9.99},
        "plan_pro": {"id": "plan_pro", "name": "Pro", "price_monthly": 19.99},
    }
    _subscriptions = {}
    _idempotency_index = {}
    _plan_price_cache = {plan_id: plan["price_monthly"] for plan_id, plan in _plans.items()}


def list_plans() -> list[dict]:
    return deepcopy(list(_plans.values()))


def get_plan(plan_id: str) -> dict | None:
    plan = _plans.get(plan_id)
    return deepcopy(plan) if plan else None


def create_plan(name: str, price_monthly: float) -> dict:
    plan_id = f"plan_{len(_plans) + 1}"
    plan = {"id": plan_id, "name": name, "price_monthly": price_monthly}
    _plans[plan_id] = plan
    _plan_price_cache[plan_id] = price_monthly
    return deepcopy(plan)


def update_plan_price(plan_id: str, price_monthly: float) -> dict | None:
    plan = _plans.get(plan_id)
    if plan is None:
        return None
    plan["price_monthly"] = price_monthly
    return deepcopy(plan)


def create_subscription(plan_id: str, customer_email: str, idempotency_key: str) -> dict:
    plan = _plans.get(plan_id)
    sub_id = f"sub_{len(_subscriptions) + 1}"
    subscription = {
        "id": sub_id,
        "plan_id": plan_id,
        "customer_email": customer_email,
        "status": "active",
        "current_plan_price": plan["price_monthly"] if plan else 0.0,
    }
    _subscriptions[sub_id] = subscription
    _idempotency_index[idempotency_key] = sub_id
    return deepcopy(subscription)


def get_subscription_by_idempotency(idempotency_key: str) -> dict | None:
    sub_id = _idempotency_index.get(idempotency_key)
    if sub_id is None:
        return None
    return get_subscription(sub_id)


def get_subscription(subscription_id: str) -> dict | None:
    subscription = _subscriptions.get(subscription_id)
    if subscription is None:
        return None
    result = deepcopy(subscription)
    result["current_plan_price"] = _plan_price_cache.get(subscription["plan_id"], 0.0)
    return result


def cancel_subscription(subscription_id: str) -> dict | None:
    subscription = _subscriptions.get(subscription_id)
    if subscription is None:
        return None
    subscription["status"] = "canceled"
    return deepcopy(subscription)


reset()
