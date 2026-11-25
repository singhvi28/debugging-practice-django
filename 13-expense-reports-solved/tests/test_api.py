import json

from tests.conftest import AUTH


def test_list_reports_is_public(client):
    res = client.get("/reports")
    assert res.status_code == 200
    assert len(res.json()) >= 2


def test_create_report_requires_auth(client):
    res = client.post(
        "/reports",
        data=json.dumps({"title": "Supplies", "owner": "carol"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_create_report_with_auth(client):
    res = client.post(
        "/reports",
        data=json.dumps({"title": "Supplies", "owner": "carol"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201


def test_submit_report(client):
    res = client.post("/reports/rep1/submit")
    assert res.status_code == 200
    assert res.json()["status"] == "submitted"


def test_approve_draft_report_returns_409(client):
    res = client.post("/reports/rep1/approve", headers=AUTH)
    assert res.status_code == 409


def test_approve_submitted_report(client):
    res = client.post("/reports/rep2/approve", headers=AUTH)
    assert res.status_code == 200
    assert res.json()["status"] == "approved"
    assert client.get("/reports/rep2").json()["status"] == "approved"


def test_add_line_to_missing_report_returns_404(client):
    res = client.post(
        "/reports/missing/lines",
        data=json.dumps({"description": "Taxi", "amount": 25.0}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 404


def test_empty_line_description_returns_400(client):
    res = client.post(
        "/reports/rep1/lines",
        data=json.dumps({"description": "", "amount": 10.0}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 400
