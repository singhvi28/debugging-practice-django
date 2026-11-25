import json

AUTH = {"Authorization": "Bearer secret-token"}


def test_search_is_case_insensitive(client):
    res = client.get("/recipes", {"search": "pasta"})
    assert res.status_code == 200
    names = [r["name"] for r in res.json()]
    assert "Pasta Carbonara" in names


def test_duplicate_ingredient_returns_409(client):
    res = client.post(
        "/recipes/r1/ingredients",
        data=json.dumps({"name": "Spaghetti", "quantity": "200g"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 409


def test_get_missing_recipe_returns_404(client):
    res = client.get("/recipes/does-not-exist")
    assert res.status_code == 404
    assert "detail" in res.json()


def test_add_ingredient_to_missing_recipe_returns_404(client):
    res = client.post(
        "/recipes/missing/ingredients",
        data=json.dumps({"name": "Salt", "quantity": "1 tsp"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 404


def test_add_ingredient_to_recipe(client):
    res = client.post(
        "/recipes/r2/ingredients",
        data=json.dumps({"name": "Chicken", "quantity": "500g"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Chicken"


def test_create_recipe_with_auth(client):
    res = client.post(
        "/recipes",
        data=json.dumps({"name": "Tomato Soup"}),
        content_type="application/json",
        headers=AUTH,
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Tomato Soup"


def test_create_recipe_without_auth_is_401(client):
    res = client.post(
        "/recipes",
        data=json.dumps({"name": "Tomato Soup"}),
        content_type="application/json",
    )
    assert res.status_code == 401
