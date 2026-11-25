from urllib.parse import parse_qs, urlparse


def test_spaces_and_ampersands_are_percent_encoded(client):
    response = client.get(
        "/search-url",
        {"q": "foo & bar", "city": "San Jose"},
    )
    payload = response.json()

    assert response.status_code == 200
    parsed = urlparse(payload["url"])
    query = parse_qs(parsed.query)

    assert query["q"] == ["foo & bar"]
    assert query["city"] == ["San Jose"]
    assert " " not in parsed.query
    assert "&bar" not in parsed.query


def test_simple_query_still_works(client):
    response = client.get("/search-url", {"q": "laptop"})
    payload = response.json()

    assert response.status_code == 200
    assert payload["url"].endswith("q=laptop&city=New+York") or payload["url"].endswith(
        "q=laptop&city=New%20York"
    )
