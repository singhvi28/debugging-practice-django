import json
import threading

from tests.conftest import AUTH


def test_balance_requires_auth(client):
    res = client.get("/accounts/acct_1/balance")
    assert res.status_code == 401
    authed = client.get("/accounts/acct_1/balance", headers=AUTH)
    assert authed.status_code == 200
    assert authed.json()["balance"] == 500


def test_redeem_requires_auth(client):
    res = client.post(
        "/accounts/acct_1/redeem",
        data=json.dumps({"amount": 10, "reason": "coffee"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_redeem_path_and_updates_balance(client):
    res = client.post(
        "/accounts/acct_1/redeem",
        data=json.dumps({"amount": 50, "reason": "gift"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    assert res.json()["balance"] == 450
    balance = client.get("/accounts/acct_1/balance", headers=AUTH)
    assert balance.json()["balance"] == 450


def test_redeem_over_balance_returns_400(client):
    res = client.post(
        "/accounts/acct_2/redeem",
        data=json.dumps({"amount": 500, "reason": "too much"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400


def test_earn_missing_account_returns_404(client):
    res = client.post(
        "/accounts/missing/earn",
        data=json.dumps({"amount": 10, "reason": "bonus"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 404


def test_concurrent_redeem_only_one_succeeds(client):
    results: list[int] = []

    def redeem():
        response = client.post(
            "/accounts/acct_2/redeem",
            data=json.dumps({"amount": 80, "reason": "race"}),
            content_type="application/json",
            headers=AUTH,
        )
        results.append(response.status_code)

    t1 = threading.Thread(target=redeem)
    t2 = threading.Thread(target=redeem)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert sorted(results) == [200, 409]
