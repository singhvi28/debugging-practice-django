from django.db import models


class Recipe(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.quantity} {self.name} for {self.recipe.name}"
