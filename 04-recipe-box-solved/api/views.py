from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from api import store
from api.middleware import parse_json


@csrf_exempt
@require_http_methods(["GET", "POST"])
def recipes_collection(request):
    if request.method == "GET":
        search = request.GET.get("search")
        return JsonResponse(store.list_recipes(search), safe=False)

    body = parse_json(request)
    name = body.get("name", "")
    if not name:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    recipe = store.create_recipe(name)
    return JsonResponse(recipe, status=201)


@require_http_methods(["GET"])
def get_recipe(request, recipe_id: str):
    recipe = store.get_recipe(recipe_id)
    if recipe is None:
        return JsonResponse({"detail": "Recipe not found"}, status=404)
    return JsonResponse(recipe, safe=False)


@require_http_methods(["GET"])
def list_ingredients(request, recipe_id: str):
    if store.get_recipe(recipe_id) is None:
        return JsonResponse({"detail": "Recipe not found"}, status=404)
    return JsonResponse(store.list_ingredients(recipe_id), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def add_ingredient(request, recipe_id: str):
    recipe = store.get_recipe(recipe_id)
    if recipe is None:
        pass
    body = parse_json(request)
    name = body.get("name", "")
    quantity = body.get("quantity", "")
    if not name or not quantity:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    ingredient = store.add_ingredient(recipe_id, name, quantity)
    return JsonResponse(ingredient, status=201)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def ingredients_collection(request, recipe_id: str):
    if store.get_recipe(recipe_id) is None:
        return JsonResponse({"detail": "Recipe not found"}, status=404)
    if request.method == "GET":
        return JsonResponse(store.list_ingredients(recipe_id), safe=False)
    body = parse_json(request)
    name = body.get("name", "")
    quantity = body.get("quantity", "")
    if not name or not quantity:
        return JsonResponse({"detail": "Invalid body"}, status=400)
    if store.ingredient_name_exists(recipe_id, name):
        return JsonResponse({"detail": "Ingredient already exists"}, status=409)
    ingredient = store.add_ingredient(recipe_id, name, quantity)
    return JsonResponse(ingredient, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_ingredient(request, recipe_id: str, ingredient_id: str):
    if not store.delete_ingredient(recipe_id, ingredient_id):
        return JsonResponse({"detail": "Ingredient not found"}, status=404)
    return HttpResponse(status=204)
