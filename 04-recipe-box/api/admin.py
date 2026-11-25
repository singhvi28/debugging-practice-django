from django.contrib import admin
from .models import Recipe, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "recipe")
    search_fields = ("name",)
