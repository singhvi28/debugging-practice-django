import json

from tests.conftest import ADMIN_AUTH, AUTH


def test_list_books(client):
    res = client.get("/books")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_book(client):
    res = client.get("/books/bk1")
    assert res.status_code == 200
    assert res.json()["title"] == "Dune"


def test_overdue_requires_admin_token(client):
    res = client.get("/loans/overdue")
    assert res.status_code == 401


def test_overdue_rejects_user_token(client):
    res = client.get("/loans/overdue", headers=AUTH)
    assert res.status_code == 401


def test_overdue_with_admin(client):
    res = client.get("/loans/overdue", headers=ADMIN_AUTH)
    assert res.status_code == 200
    ids = [loan["id"] for loan in res.json()]
    assert "ln1" in ids


def test_return_loan_via_post(client):
    res = client.post("/loans/ln1/return")
    assert res.status_code == 200
    assert res.json()["id"] == "ln1"


def test_max_active_loans_returns_409(client):
    res = client.post(
        "/loans",
        data=json.dumps({"book_id": "bk1", "user_id": "user2"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_return_missing_loan_returns_404(client):
    res = client.post("/loans/missing-loan/return")
    assert res.status_code == 404


def test_create_loan_persists(client):
    res = client.post(
        "/loans",
        data=json.dumps({"book_id": "bk1", "user_id": "new-borrower"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    loans = client.get("/loans").json()
    assert any(loan["user_id"] == "new-borrower" for loan in loans)


def test_returned_loan_not_in_overdue(client):
    client.post("/loans/ln1/return")
    res = client.get("/loans/overdue", headers=ADMIN_AUTH)
    ids = [loan["id"] for loan in res.json()]
    assert "ln1" not in ids


def test_create_loan_without_auth_is_401(client):
    res = client.post(
        "/loans",
        data=json.dumps({"book_id": "bk1", "user_id": "guest"}),
        content_type="application/json",
    )
    assert res.status_code == 401
