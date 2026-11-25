import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/books", {"search": "hobbit"})
    assert res.status_code == 200
    titles = [b["title"] for b in res.json()]
    assert "The Hobbit" in titles


def test_search_partial_match(client):
    res = client.get("/books", {"search": "neuro"})
    assert res.status_code == 200
    titles = [b["title"] for b in res.json()]
    assert "Neuromancer" in titles


def test_empty_search_returns_all(client):
    res = client.get("/books")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_missing_book_returns_404(client):
    res = client.get("/books/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_create_book_returns_201(client):
    res = client.post(
        "/books",
        data=json.dumps({"title": "Foundation", "author": "Asimov"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["title"] == "Foundation"


def test_create_book_without_auth_is_401(client):
    res = client.post(
        "/books",
        data=json.dumps({"title": "Foundation", "author": "Asimov"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_delete_book_with_auth(client):
    res = client.delete("/books/b2", headers=AUTH)
    assert res.status_code == 204
    assert client.get("/books/b2").status_code == 404


def test_remove_cart_item_keeps_other_items(client):
    client.post(
        "/cart/c1/items",
        data=json.dumps({"book_id": "b2"}),
        content_type="application/json",
        headers=AUTH,
    )
    res = client.delete("/cart/c1/items/b1", headers=AUTH)
    assert res.status_code == 204
    cart = client.get("/cart/c1").json()
    book_ids = [i["book_id"] for i in cart["items"]]
    assert "b1" not in book_ids
    assert "b2" in book_ids


def test_authenticated_cart_add_works(client):
    res = client.post(
        "/cart/c1/items",
        data=json.dumps({"book_id": "b3"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 200
    book_ids = [i["book_id"] for i in res.json()["items"]]
    assert "b3" in book_ids
