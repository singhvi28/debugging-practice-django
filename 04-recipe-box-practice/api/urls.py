from django.urls import path

from api import views

urlpatterns = [
    path("recipes", views.recipes_collection),
    path("recipes/<str:recipe_id>", views.get_recipe),
    path("recipes/<str:recipe_id>/ingredients", views.list_ingredients),
    path("recipes/<str:recipe_id>/ingredients", views.add_ingredient),
    path(
        "recipes/<str:recipe_id>/ingredients/<str:ingredient_id>",
        views.delete_ingredient,
    ),
]
