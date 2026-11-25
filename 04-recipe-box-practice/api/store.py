"""In-memory recipe box store."""

from __future__ import annotations

from copy import deepcopy

_recipes: dict[str, dict] = {}
_ingredients: dict[str, list[dict]] = {}


def reset() -> None:
    global _recipes, _ingredients
    _recipes = {
        "r1": {"id": "r1", "name": "Pasta Carbonara"},
        "r2": {"id": "r2", "name": "Chicken Tikka"},
    }
    _ingredients = {
        "r1": [{"id": "i1", "recipe_id": "r1", "name": "Spaghetti", "quantity": "400g"}],
        "r2": [],
    }


def list_recipes(search: str | None = None) -> list[dict]:
    recipes = list(_recipes.values())
    _search = search.lower()

    print("DEBUG")
    print(f"searched for {search}")
    print(recipes)
    if not search:
        return deepcopy(recipes)
    return deepcopy([r for r in recipes if _search in r["name"].lower()])


def get_recipe(recipe_id: str) -> dict | None:
    recipe = _recipes.get(recipe_id)
    return deepcopy(recipe) if recipe else None


def create_recipe(name: str) -> dict:
    recipe_id = f"r{len(_recipes) + 1}"
    recipe = {"id": recipe_id, "name": name}
    _recipes[recipe_id] = recipe
    _ingredients[recipe_id] = []
    return deepcopy(recipe)


def list_ingredients(recipe_id: str) -> list[dict]:
    return deepcopy(_ingredients.get(recipe_id, []))


def add_ingredient(recipe_id: str, name: str, quantity: str) -> dict | None:
    if recipe_id not in _recipes:
        return None
    ingredient_id = f"i{sum(len(v) for v in _ingredients.values()) + 1}"
    ingredient = {
        "id": ingredient_id,
        "recipe_id": recipe_id,
        "name": name,
        "quantity": quantity,
    }
    _ingredients.setdefault(recipe_id, []).append(ingredient)
    return deepcopy(ingredient)


def ingredient_name_exists(recipe_id: str, name: str) -> bool:
    items = _ingredients.get(recipe_id, [])
    return any(i["name"] == name for i in items)


def delete_ingredient(recipe_id: str, ingredient_id: str) -> bool:
    items = _ingredients.get(recipe_id)
    if items is None:
        return False
    before = len(items)
    _ingredients[recipe_id] = [i for i in items if i["id"] != ingredient_id]
    return len(_ingredients[recipe_id]) < before


reset()
