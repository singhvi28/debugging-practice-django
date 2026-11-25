import json
import threading

from django.test import Client

from register_helper import reset


def test_duplicate_registration_rejected(client):
    first = client.post(
        "/register",
        data=json.dumps({"email": "alice@example.com"}),
        content_type="application/json",
    )
    second = client.post(
        "/register",
        data=json.dumps({"email": "alice@example.com"}),
        content_type="application/json",
    )
    assert first.status_code == 200
    assert second.status_code == 409


def test_concurrent_same_email_only_one_succeeds():
    reset()
    email = "race@example.com"
    results: list[int] = []
    barrier = threading.Barrier(2)

    def attempt():
        barrier.wait()
        c = Client()
        res = c.post(
            "/register",
            data=json.dumps({"email": email}),
            content_type="application/json",
        )
        results.append(res.status_code)

    threads = [threading.Thread(target=attempt) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sorted(results) == [200, 409]


def test_distinct_emails_both_succeed(client):
    a = client.post(
        "/register",
        data=json.dumps({"email": "a@example.com"}),
        content_type="application/json",
    )
    b = client.post(
        "/register",
        data=json.dumps({"email": "b@example.com"}),
        content_type="application/json",
    )
    assert a.status_code == 200
    assert b.status_code == 200
    assert client.get("/users/count").json()["count"] == 2
