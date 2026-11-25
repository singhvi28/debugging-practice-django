import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/movies", {"search": "interstellar"})
    assert res.status_code == 200
    titles = [m["title"] for m in res.json()]
    assert "Interstellar" in titles


def test_search_partial_match(client):
    res = client.get("/movies", {"search": "dark"})
    assert res.status_code == 200
    titles = [m["title"] for m in res.json()]
    assert "The Dark Knight" in titles


def test_empty_search_returns_all(client):
    res = client.get("/movies")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_missing_movie_returns_404(client):
    res = client.get("/movies/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_review_for_missing_movie_returns_404(client):
    res = client.post(
        "/movies/missing/reviews",
        data=json.dumps({"rating": 4, "text": "ok"}),
        content_type="application/json",
    )
    assert res.status_code == 404


def test_watchlist_rejects_duplicate_movie(client):
    res = client.post(
        "/watchlists/w1/movies",
        data=json.dumps({"movie_id": "m1"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_delete_movie_with_auth(client):
    res = client.delete("/movies/m2", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/movies/m2").status_code == 404


def test_authenticated_create_movie(client):
    res = client.post(
        "/movies",
        data=json.dumps({"title": "Dune", "year": 2021}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["title"] == "Dune"


def test_create_movie_without_auth_is_401(client):
    res = client.post(
        "/movies",
        data=json.dumps({"title": "Dune", "year": 2021}),
        content_type="application/json",
    )
    assert res.status_code == 401
