from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class StockMove(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="moves")
    change_type = models.CharField(max_length=32)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change_type} {self.quantity} ({self.product.sku})"
