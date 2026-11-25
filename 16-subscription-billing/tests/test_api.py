import json

from tests.conftest import ADMIN, AUTH


def test_post_plans_rejects_secret_token(client):
    res = client.post(
        "/plans",
        data=json.dumps({"name": "Enterprise", "price_monthly": 49.99}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 403


def test_post_plans_with_admin_token(client):
    res = client.post(
        "/plans",
        data=json.dumps({"name": "Enterprise", "price_monthly": 49.99}),
        content_type="application/json",
        headers=ADMIN,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Enterprise"


def test_cancel_subscription_path(client):
    sub = client.post(
        "/subscriptions",
        data=json.dumps({"plan_id": "plan_basic", "customer_email": "a@example.com"}),
        content_type="application/json",
        headers={**AUTH, "Idempotency-Key": "cancel-path-key"},
    ).json()
    res = client.post(f"/subscriptions/{sub['id']}/cancel", headers=AUTH)
    assert res.status_code == 200
    assert res.json()["status"] == "canceled"


def test_subscribe_idempotency_returns_same_subscription(client):
    body = {"plan_id": "plan_pro", "customer_email": "idem@example.com"}
    headers = {**AUTH, "Idempotency-Key": "idem-123"}
    first = client.post(
        "/subscriptions",
        data=json.dumps(body),
        content_type="application/json",
        headers=headers,
    )
    second = client.post(
        "/subscriptions",
        data=json.dumps(body),
        content_type="application/json",
        headers=headers,
    )
    assert first.status_code == 201
    assert second.status_code in (200, 201)
    assert first.json()["id"] == second.json()["id"]


def test_subscribe_missing_plan_returns_404(client):
    res = client.post(
        "/subscriptions",
        data=json.dumps({"plan_id": "missing", "customer_email": "x@example.com"}),
        content_type="application/json",
        headers={**AUTH, "Idempotency-Key": "missing-plan"},
    )
    assert res.status_code == 404


def test_cancel_already_canceled_returns_409(client):
    sub = client.post(
        "/subscriptions",
        data=json.dumps({"plan_id": "plan_basic", "customer_email": "c@example.com"}),
        content_type="application/json",
        headers={**AUTH, "Idempotency-Key": "double-cancel"},
    ).json()
    client.post(f"/subscriptions/{sub['id']}/cancel", headers=AUTH)
    res = client.post(f"/subscriptions/{sub['id']}/cancel", headers=AUTH)
    assert res.status_code == 409


def test_subscription_reflects_updated_plan_price(client):
    sub = client.post(
        "/subscriptions",
        data=json.dumps({"plan_id": "plan_basic", "customer_email": "price@example.com"}),
        content_type="application/json",
        headers={**AUTH, "Idempotency-Key": "price-cache"},
    ).json()
    client.patch(
        "/plans/plan_basic/price",
        data=json.dumps({"price_monthly": 12.50}),
        content_type="application/json",
        headers=ADMIN,
    )
    res = client.get(f"/subscriptions/{sub['id']}")
    assert res.status_code == 200
    assert res.json()["current_plan_price"] == 12.50
