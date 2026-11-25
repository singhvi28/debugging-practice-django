from django.test import Client

client = Client()

ORIGIN = {"Origin": "https://app.example.com"}


def test_actual_response_exposes_custom_headers():
    response = client.get("/profile", headers=ORIGIN)
    assert response.status_code == 200
    assert response.headers.get("access-control-expose-headers") == "X-Request-Id, X-RateLimit-Remaining"


def test_preflight_declares_exposed_headers():
    response = client.options(
        "/profile",
        headers={
            **ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 204
    assert response.headers.get("access-control-expose-headers") == "X-Request-Id, X-RateLimit-Remaining"


def test_untrusted_origin_gets_no_cors_headers():
    response = client.options(
        "/profile",
        headers={"Origin": "https://evil.example.com"},
    )
    assert "access-control-expose-headers" not in response.headers
